# Vigia do robô

Mostra com quem o robô de IA conversa pela internet, quanto ele manda e em que minutos —
inclusive quando ninguém está falando com ele. Tudo local: sem conta, sem serviço externo.

**Para quem:** pai, mãe ou professor com um notebook Linux (ou um adolescente que goste de
computador). Quem não tem isso pode usar o app do roteador, que costuma mostrar o consumo de
dados por aparelho (procure por "dispositivos" ou "consumo").

## Antes de começar

- **Linux com NetworkManager** (Ubuntu, Mint, Fedora). Windows e Mac não estão cobertos.
- **tcpdump** instalado: `sudo apt install tcpdump` (Ubuntu/Mint) ou `sudo dnf install tcpdump` (Fedora).
- **Internet por cabo** no notebook (ou uma 2ª placa Wi-Fi): a placa Wi-Fi vira a rede do robô e
  deixa de ser a internet. Sem cabo, o robô fica sem internet e o relatório sai vazio.
- **sudo** para a captura ao vivo. O relatório sai em português.
- A senha da rede `ROBO-VIGIA` é aleatória a cada vez (aparece na tela); para fixar, use
  `SENHA_HOTSPOT=suasenha ./hotspot.sh --ligar`.

## O processo, do início ao fim

| # | Passo | Comando | Quem |
|---|---|---|---|
| 1 | Testar o vigia sem robô (captura inventada) | `./teste.sh` | ⚙️ script |
| 2 | Ligar o notebook como rede Wi-Fi do robô | `./hotspot.sh --ligar` | 🧠 você |
| 3 | Trocar a Wi-Fi do robô para `ROBO-VIGIA` no app dele | — | 🧠 você |
| 4 | Achar o endereço do robô | `./hotspot.sh --clientes` | ⚙️ script |
| 5 | Vigiar enquanto a criança usa (ou em silêncio, por 10 min) | `sudo python3 vigia_robo.py --iface <placa> --ip <endereço> --saida relatorio.md` | ⚙️ script |
| 6 | Ler o relatório: destinos, empresas, país da empresa, envio minuto a minuto | abrir `relatorio.md` | 🧠 você |
| 7 | Desligar o hotspot | `./hotspot.sh --desligar` | ⚙️ script |

Dica de teste: deixe o robô **10 minutos ligado sem ninguém falar**. Se o gráfico minuto a
minuto mostrar envio grande nesses minutos, ele está mandando dados sozinho.

## O que ele lê e o que não lê

- Lê **para onde** os pacotes vão, **quanto** vai e os **nomes** que o robô pergunta ao DNS.
- **Não** lê o conteúdo (a voz vai criptografada). O vigia prova o caminho, não o que foi dito.
- O país é o da **empresa** dona do nome, pela lista `dominios.json` (curta, corrija à vontade).
  Endereço sem nome aparece como "não identificado": o robô usou um endereço fixo.
- Tamanhos são aproximados (conteúdo dos pacotes, sem cabeçalhos).

## Arquivos

- `vigia_robo.py` — o vigia (`--iface` ao vivo com sudo, `--pcap` de captura gravada, `--stdin`).
- `hotspot.sh` — liga/desliga a rede `ROBO-VIGIA` pelo NetworkManager e lista quem está ligado.
- `dominios.json` — nome → empresa e país da empresa.
- `exemplo/` — gerador de captura **inventada** (endereços de documentação) e o relatório dela.
- `teste.sh` — 7 testes com o exemplo.

## Estado

- ✅ Testado: leitura de captura, nomes via DNS, endereço sem nome, porcentagem, gráfico.
- 🔶 A testar ao vivo: `hotspot.sh` e a captura com um robô de verdade (vamos fazer com o Bean Bun).
