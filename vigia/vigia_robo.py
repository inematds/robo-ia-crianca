#!/usr/bin/env python3
"""Vigia do robô: mostra com quem o robô de IA conversa pela internet e quanto ele manda.

Não precisa de nenhuma conta nem serviço externo: lê o tráfego com o tcpdump e cruza os
nomes que o próprio robô pergunta ao DNS com a lista dominios.json.

Uso:
  sudo python3 vigia_robo.py --iface wlan0 --ip 10.42.0.50      # ao vivo (Ctrl+C encerra)
  python3 vigia_robo.py --pcap captura.pcap --ip 10.42.0.50     # captura gravada (sem sudo)
  python3 vigia_robo.py --pcap exemplo/exemplo.pcap --ip 10.42.0.50 --saida relatorio.md

Para ver o tráfego, o computador precisa estar no caminho do robô: ligue o robô num
hotspot do próprio computador (veja hotspot.sh) ou capture no roteador.
"""
import argparse
import json
import shlex
import shutil
import threading
import os
import re
import signal
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent

RE_LINHA = re.compile(r"^(\d+\.\d+)\s+(IP6?)\s+(\S+)\s+>\s+(\S+?):\s*(.*)$")
RE_DNS_PERGUNTA = re.compile(r"^(\d+)\+?\s+(?:\[[^\]]*\]\s+)?(?:A|AAAA|HTTPS)\?\s+(\S+?)\.?\s")
RE_DNS_RESPOSTA = re.compile(r"^(\d+)[*\-|$]*\s+(?:q:\s+\S+\s+\S+\s+)?\d+/\d+/\d+\s+(.*)$")
RE_ENDERECO = re.compile(r"\b(?:A|AAAA)\s+([0-9a-fA-F:.]+?)(?:,|\s|\()")
RE_TAMANHO = re.compile(r"length\s+(\d+)")
RE_TAMANHO_DNS = re.compile(r"\((\d+)\)\s*$")


def separa(endereco):
    """'10.42.0.50.443' -> ('10.42.0.50', '443'); IPv6 também termina em .porta."""
    if "." not in endereco:
        return endereco, ""
    host, porta = endereco.rsplit(".", 1)
    if not porta.isdigit():
        return endereco, ""
    return host, porta


def eh_local(end):
    if end.startswith(("10.", "192.168.", "169.254.", "fe80:")):
        return True
    if end.startswith("172."):
        try:
            return 16 <= int(end.split(".")[1]) <= 31
        except (IndexError, ValueError):
            return False
    return False


def carrega_dominios(caminho):
    dados = json.loads(Path(caminho).read_text(encoding="utf-8"))
    return {k.lower(): v for k, v in dados.items() if not k.startswith("_")}


def identifica(nome, dominios):
    if not nome:
        return {"quem": "não identificado (endereço fixo, sem perguntar o nome)", "pais": "?"}
    nome = nome.lower().rstrip(".")
    partes = nome.split(".")
    for i in range(len(partes)):
        sufixo = ".".join(partes[i:])
        if sufixo in dominios:
            return dominios[sufixo]
    return {"quem": "não identificado", "pais": "?"}


class Vigia:
    def __init__(self, ip_robo, dominios):
        self.ip = ip_robo
        self.dominios = dominios
        self.perguntas = {}          # id da pergunta DNS -> nome
        self.nome_do_ip = {}         # ip -> nome perguntado
        self.enviado = defaultdict(int)
        self.recebido = defaultdict(int)
        self.pacotes = defaultdict(int)
        self.por_minuto = defaultdict(int)
        self.nomes_pedidos = []
        self.inicio = None
        self.fim = None
        self.linhas = 0

    def linha(self, texto):
        m = RE_LINHA.match(texto.strip())
        if not m:
            return
        quando, _, origem, destino, resto = m.groups()
        quando = float(quando)
        src, sport = separa(origem)
        dst, dport = separa(destino)
        if self.ip not in (src, dst):
            return
        self.linhas += 1
        self.inicio = quando if self.inicio is None else min(self.inicio, quando)
        self.fim = quando if self.fim is None else max(self.fim, quando)

        if dport == "53" and src == self.ip:
            p = RE_DNS_PERGUNTA.match(resto)
            if p:
                self.perguntas[p.group(1)] = p.group(2).rstrip(".")
                if p.group(2).rstrip(".") not in self.nomes_pedidos:
                    self.nomes_pedidos.append(p.group(2).rstrip("."))
        if sport == "53" and dst == self.ip:
            r = RE_DNS_RESPOSTA.match(resto)
            if r and r.group(1) in self.perguntas:
                nome = self.perguntas[r.group(1)]
                for end in RE_ENDERECO.findall(r.group(2) + " "):
                    self.nome_do_ip[end] = nome

        tamanhos = RE_TAMANHO.findall(resto)
        if tamanhos:
            tam = int(tamanhos[-1])
        else:
            d = RE_TAMANHO_DNS.search(resto)
            tam = int(d.group(1)) if d else 0
        if src == self.ip:
            outro = dst
            self.enviado[outro] += tam
            self.por_minuto[int(quando // 60)] += tam
        else:
            outro = src
            self.recebido[outro] += tam
        self.pacotes[outro] += 1

    def destinos(self):
        lista = []
        for end in set(self.enviado) | set(self.recebido):
            nome = self.nome_do_ip.get(end, "")
            info = identifica(nome, self.dominios)
            if eh_local(end) and not nome:
                info = {"quem": "rede local (roteador / DNS de casa)", "pais": "casa"}
            lista.append({
                "endereco": end, "nome": nome, "quem": info["quem"], "pais": info["pais"],
                "enviado": self.enviado[end], "recebido": self.recebido[end],
                "pacotes": self.pacotes[end],
            })
        lista.sort(key=lambda d: d["enviado"], reverse=True)
        return lista

    def relatorio(self):
        if not self.linhas:
            return ("Nenhum pacote do robô apareceu. Confira o --ip do robô e se o computador está "
                    "no caminho dele (hotspot.sh --clientes mostra quem está ligado).\n")
        d = self.destinos()
        fora = [x for x in d if x["pais"] != "casa"]
        total = sum(x["enviado"] for x in fora) or 1
        china = sum(x["enviado"] for x in d if x["pais"].startswith("China"))
        nao_id = sum(x["enviado"] for x in fora if x["pais"] == "?")
        local = sum(x["enviado"] for x in d if x["pais"] == "casa")
        dur = (self.fim - self.inicio) if self.fim and self.inicio else 0
        out = []
        out.append("# Vigia do robô — relatório\n")
        out.append(f"- Robô: `{self.ip}`")
        out.append(f"- Tempo observado: {dur/60:.1f} min · {self.linhas} pacotes")
        out.append(f"- Enviado pelo robô para fora de casa: **{kb(total if fora else 0)}** "
                   f"para {len(fora)} destino(s) (mais {kb(local)} dentro da rede de casa)")
        out.append(f"- Para empresas da China (pela lista): **{china*100//total}%**")
        if nao_id:
            out.append(f"- Para destinos não identificados: {nao_id*100//total}% (veja a tabela)")
        if self.nomes_pedidos:
            out.append(f"- Nomes que o robô procurou: {', '.join(self.nomes_pedidos)}")
        out.append("")
        out.append("| Destino | Quem | País da empresa | Enviado | Recebido | Pacotes |")
        out.append("|---|---|---|---:|---:|---:|")
        for x in d:
            alvo = f"{x['nome']} ({x['endereco']})" if x["nome"] else x["endereco"]
            out.append(f"| {alvo} | {x['quem']} | {x['pais']} | {kb(x['enviado'])} | "
                       f"{kb(x['recebido'])} | {x['pacotes']} |")
        out.append("")
        out.append("## Envio minuto a minuto")
        out.append("Se aparece envio em minutos em que ninguém falou com o robô, ele está mandando dados sozinho.\n")
        out.append("```")
        maior = max(self.por_minuto.values() or [1])
        for minuto in sorted(self.por_minuto):
            hora = time.strftime("%H:%M", time.localtime(minuto * 60))
            barra = "█" * max(1, round(30 * self.por_minuto[minuto] / maior))
            out.append(f"{hora}  {barra} {kb(self.por_minuto[minuto])}")
        out.append("```")
        out.append("\nTamanhos aproximados (conteúdo dos pacotes, sem cabeçalhos). "
                   "Lista de nomes: dominios.json. Guia: https://inematds.github.io/robo-ia-crianca/guia/")
        return "\n".join(out) + "\n"


def kb(n):
    if n >= 1024 * 1024:
        return f"{n/1024/1024:.1f} MB"
    if n >= 1024:
        return f"{n/1024:.1f} KB"
    return f"{n} B"


def main():
    ap = argparse.ArgumentParser(description="Mostra com quem o robô conversa pela internet.")
    ap.add_argument("--ip", required=True, help="endereço do robô na rede (ex.: 10.42.0.50)")
    fonte = ap.add_mutually_exclusive_group(required=True)
    fonte.add_argument("--iface", help="placa de rede para capturar ao vivo (precisa de sudo)")
    fonte.add_argument("--pcap", help="arquivo de captura já gravado (.pcap)")
    fonte.add_argument("--stdin", action="store_true", help="ler a saída de 'tcpdump -nn -l -tt' da entrada")
    ap.add_argument("--saida", help="grava o relatório neste arquivo .md")
    ap.add_argument("--gravar", help="ao vivo: grava também a captura neste .pcap")
    ap.add_argument("--minutos", type=float, help="ao vivo: para sozinho depois de N minutos")
    ap.add_argument("--dominios", default=str(AQUI / "dominios.json"))
    a = ap.parse_args()

    vigia = Vigia(a.ip, carrega_dominios(a.dominios))
    if not a.stdin and not shutil.which("tcpdump"):
        sys.exit("Falta o tcpdump. Instale com: sudo apt install tcpdump (Ubuntu/Mint) "
                 "ou sudo dnf install tcpdump (Fedora).")
    erros = ""

    if a.stdin:
        for t in sys.stdin:
            vigia.linha(t)
    else:
        if a.pcap:
            if not os.path.isfile(a.pcap):
                sys.exit(f"Arquivo não encontrado: {a.pcap}")
            cmd = ["tcpdump", "-nn", "-l", "-tt", "-r", a.pcap, "host", a.ip]
        else:
            if os.geteuid() != 0:
                sys.exit("Captura ao vivo precisa de sudo: sudo python3 vigia_robo.py --iface ... --ip ...")
            cmd = ["tcpdump", "-nn", "-l", "-tt", "-i", a.iface, "host", a.ip]
            if a.gravar:
                # grava o pcap e lê o texto ao mesmo tempo
                i, h, g = shlex.quote(a.iface), shlex.quote(a.ip), shlex.quote(a.gravar)
                cmd = ["sh", "-c", f"tcpdump -nn -U -i {i} -w - host {h} | tee {g} | tcpdump -nn -l -tt -r -"]
            print(f"Vigiando {a.ip} em {a.iface}. Use o robô normalmente; Ctrl+C para o relatório.",
                  file=sys.stderr)
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                start_new_session=True)
        parar = lambda *_: os.killpg(proc.pid, signal.SIGTERM) if proc.poll() is None else None
        coletado = []
        leitor = threading.Thread(target=lambda: coletado.append(proc.stderr.read()), daemon=True)
        leitor.start()
        if a.minutos:
            # para no horário mesmo que o robô fique em silêncio total
            relogio = threading.Timer(a.minutos * 60, parar)
            relogio.daemon = True
            relogio.start()
        signal.signal(signal.SIGINT, parar)
        try:
            for t in proc.stdout:
                vigia.linha(t)
        finally:
            proc.wait()
            leitor.join(timeout=2)
        erros = "".join(coletado)

    texto = vigia.relatorio()
    if not vigia.linhas and erros.strip():
        avisos = [l for l in erros.splitlines() if l.strip() and "listening on" not in l
                  and "packets" not in l and "reading from" not in l]
        if avisos:
            texto += "\nO tcpdump avisou (confira o nome da placa e a permissão):\n  " + "\n  ".join(avisos[:5]) + "\n"
    print(texto)
    if a.saida:
        Path(a.saida).write_text(texto, encoding="utf-8")
        # rodando com sudo, devolve o arquivo para quem chamou
        if os.geteuid() == 0 and os.environ.get("SUDO_UID"):
            os.chown(a.saida, int(os.environ["SUDO_UID"]), int(os.environ.get("SUDO_GID", "0")))
        print(f"Relatório salvo em {a.saida}", file=sys.stderr)


if __name__ == "__main__":
    main()
