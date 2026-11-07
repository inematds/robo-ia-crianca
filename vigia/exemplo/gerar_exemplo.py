#!/usr/bin/env python3
"""Gera exemplo.pcap: uma captura INVENTADA para testar o vigia sem ter o robô.

Os endereços são de documentação (203.0.113.x, 198.51.100.x), não são servidores reais.
Os nomes imitam o que um robô desses costuma procurar. Não é medição de nenhum aparelho.
"""
import struct
import sys
from pathlib import Path

ROBO = "10.42.0.50"
ROTEADOR = "10.42.0.1"
MAC_ROBO = bytes.fromhex("24ec4a000050")
MAC_PC = bytes.fromhex("aabbccddee01")
INICIO = 1794038400  # 07/11/2026 00:00 UTC (só o relógio do exemplo)


def ip4(s):
    return bytes(int(x) for x in s.split("."))


def soma(dados):
    if len(dados) % 2:
        dados += b"\0"
    s = sum(struct.unpack(f"!{len(dados)//2}H", dados))
    while s >> 16:
        s = (s & 0xFFFF) + (s >> 16)
    return (~s) & 0xFFFF


def ipv4(src, dst, proto, corpo):
    cab = struct.pack("!BBHHHBBH4s4s", 0x45, 0, 20 + len(corpo), 1, 0, 64, proto, 0, ip4(src), ip4(dst))
    cab = cab[:10] + struct.pack("!H", soma(cab)) + cab[12:]
    return cab + corpo


def udp(src, dst, sp, dp, dados):
    return ipv4(src, dst, 17, struct.pack("!HHHH", sp, dp, 8 + len(dados), 0) + dados)


def tcp(src, dst, sp, dp, dados, seq=1):
    cab = struct.pack("!HHIIBBHHH", sp, dp, seq, 1, 5 << 4, 0x18, 65535, 0, 0)
    return ipv4(src, dst, 6, cab + dados)


def nome_dns(nome):
    return b"".join(bytes([len(p)]) + p.encode() for p in nome.split(".")) + b"\0"


def dns_pergunta(ident, nome):
    return struct.pack("!HHHHHH", ident, 0x0100, 1, 0, 0, 0) + nome_dns(nome) + struct.pack("!HH", 1, 1)


def dns_resposta(ident, nome, endereco):
    q = nome_dns(nome) + struct.pack("!HH", 1, 1)
    r = struct.pack("!HHHIH", 0xC00C, 1, 1, 300, 4) + ip4(endereco)
    return struct.pack("!HHHHHH", ident, 0x8180, 1, 1, 0, 0) + q + r


def main(destino):
    pacotes = []

    def add(t, quadro_ip, do_robo=True):
        eth = (MAC_PC if do_robo else MAC_ROBO) + (MAC_ROBO if do_robo else MAC_PC) + b"\x08\x00"
        pacotes.append((INICIO + t, eth + quadro_ip))

    servidores = [
        ("api.tenclass.net", "203.0.113.10", 0x1111),
        ("ark.cn-beijing.volces.com", "203.0.113.20", 0x2222),
        ("api.deepseek.com", "203.0.113.30", 0x3333),
        ("pool.ntp.org", "198.51.100.5", 0x4444),
    ]
    t = 1.0
    for nome, end, ident in servidores:
        add(t, udp(ROBO, ROTEADOR, 40000 + ident % 1000, 53, dns_pergunta(ident, nome)))
        add(t + 0.02, udp(ROTEADOR, ROBO, 53, 40000 + ident % 1000, dns_resposta(ident, nome, end)), False)
        t += 0.5
    add(4.0, udp(ROBO, "198.51.100.5", 123, 123, b"\x23" + b"\0" * 47))

    # minuto 0 a 4: conversas (a voz sobe em pedaços de ~1 KB)
    for minuto, falas in [(0, 30), (1, 60), (2, 10), (4, 45)]:
        for i in range(falas):
            ts = minuto * 60 + 10 + i * 0.4
            add(ts, tcp(ROBO, "203.0.113.10", 51000, 443, b"v" * 1024, seq=i))
            if i % 5 == 0:
                add(ts + 0.1, tcp("203.0.113.10", ROBO, 443, 51000, b"r" * 600), False)
        add(minuto * 60 + 40, tcp(ROBO, "203.0.113.20", 51001, 443, b"t" * 800))
        add(minuto * 60 + 41, tcp("203.0.113.20", ROBO, 443, 51001, b"a" * 4000), False)
    # minuto 3: ninguém falou, mas ele manda sinal de vida
    for i in range(6):
        add(180 + i * 10, tcp(ROBO, "203.0.113.10", 51000, 443, b"k" * 120))
    # endereço fixo, sem perguntar nome
    for i in range(8):
        add(200 + i * 20, tcp(ROBO, "198.51.100.77", 52000, 8883, b"m" * 300))
    add(250, tcp(ROBO, "203.0.113.30", 51002, 443, b"d" * 500))

    pacotes.sort(key=lambda p: p[0])
    with open(destino, "wb") as f:
        f.write(struct.pack("<IHHiIII", 0xA1B2C3D4, 2, 4, 0, 0, 65535, 1))
        for ts, dados in pacotes:
            seg = int(ts)
            us = int(round((ts - seg) * 1e6))
            f.write(struct.pack("<IIII", seg, us, len(dados), len(dados)) + dados)
    print(f"{len(pacotes)} pacotes em {destino}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).with_name("exemplo.pcap")))
