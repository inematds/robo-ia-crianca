# Robot Network Monitor

Shows whom the AI robot talks to over the internet, how much data it sends, and in which minutes—even when no one is talking to it. Everything runs locally: no account or external service needed.

**For:** a parent or teacher with a Linux laptop (or a teenager who likes computers). If you don’t have one, you can use your router’s app, which usually shows data usage by device (look for “devices” or “usage”).

## Before you start

- **Linux with NetworkManager** (Ubuntu, Mint, Fedora). Windows and Mac are not covered.
- **tcpdump** installed: `sudo apt install tcpdump` (Ubuntu/Mint) or `sudo dnf install tcpdump` (Fedora).
- **Wired internet** on the laptop (or a second Wi-Fi adapter): the Wi-Fi adapter becomes the robot’s network and is no longer available for internet access. Without a wired connection, the robot won’t have internet and the report will be empty.
- **sudo** for live capture. The report is in Portuguese.
- The `ROBO-VIGIA` network password is random each time (it appears on screen). To set a fixed password, use
  `SENHA_HOTSPOT=yourpassword ./hotspot.sh --ligar`.

## The process, from start to finish

| # | Step | Command | Who |
|---|---|---|---|
| 1 | Test the network monitor without a robot (using a made-up capture) | `./teste.sh` | ⚙️ script |
| 2 | Turn the laptop into the robot’s Wi-Fi network | `./hotspot.sh --ligar` | 🧠 you |
| 3 | Change the robot’s Wi-Fi network to `ROBO-VIGIA` in its app | — | 🧠 you |
| 4 | Find the robot’s address | `./hotspot.sh --clientes` | ⚙️ script |
| 5 | Monitor while the child uses it (or in silence for 10 minutes) | `sudo python3 vigia_robo.py --iface <placa> --ip <endereço> --saida relatorio.md` | ⚙️ script |
| 6 | Read the report: destinations, companies, company country, minute-by-minute uploads | Open `relatorio.md` | 🧠 you |
| 7 | Turn off the hotspot | `./hotspot.sh --desligar` | ⚙️ script |

Test tip: leave the robot **on for 10 minutes without anyone talking**. If the minute-by-minute graph shows large uploads during those minutes, it’s sending data on its own.

## What it reads and what it doesn’t

- Reads **where** the packets go, **how much** data is sent, and the **names** the robot asks DNS about.
- It does **not** read the content (voice data is encrypted). The network monitor shows the route, not what was said.
- The country is the country of the **company** that owns the name, according to `dominios.json` (a short list you can edit as needed).
  An address without a name appears as “unidentified”: the robot used a fixed address.
- Sizes are approximate (packet contents, without headers).

## Files

- `vigia_robo.py` — the network monitor (`--iface` for live capture with sudo, `--pcap` for a saved capture, `--stdin`).
- `hotspot.sh` — turns the `ROBO-VIGIA` network on/off through NetworkManager and lists connected devices.
- `dominios.json` — name → company and company country.
- `exemplo/` — generator for a **made-up** capture (documentation addresses) and its report.
- `teste.sh` — 7 tests using the example.

## Status

- ✅ Tested: reading a capture, names via DNS, address without a name, percentage, graph.
- 🔶 To test live: `hotspot.sh` and capture with a real robot (we’ll do this with Bean Bun).
