# Vigía del robot

Muestra con quién se comunica el robot de IA por internet, cuántos datos envía y en qué minutos, incluso cuando nadie está hablando con él. Todo es local: sin cuenta ni servicios externos.

**Para quién:** madres, padres o docentes con una notebook Linux (o un adolescente a quien le guste la computación). Quienes no tengan una pueden usar la aplicación del router, que suele mostrar el consumo de datos por dispositivo (busca «dispositivos» o «consumo»).

## Antes de empezar

- **Linux con NetworkManager** (Ubuntu, Mint, Fedora). Windows y Mac no están incluidos.
- **tcpdump** instalado: `sudo apt install tcpdump` (Ubuntu/Mint) o `sudo dnf install tcpdump` (Fedora).
- **Internet por cable** en la notebook (o una segunda tarjeta Wi-Fi): la tarjeta Wi-Fi se convierte en la red del robot y deja de ser la conexión a internet. Sin cable, el robot se queda sin internet y el informe queda vacío.
- **sudo** para la captura en vivo. El informe sale en portugués.
- La contraseña de la red `ROBO-VIGIA` es aleatoria cada vez (aparece en pantalla); para fijarla, usa `SENHA_HOTSPOT=suasenha ./hotspot.sh --ligar`.

## El proceso, de principio a fin

| # | Paso | Comando | Quién |
|---|---|---|---|
| 1 | Probar el vigía de red sin robot (captura inventada) | `./teste.sh` | ⚙️ script |
| 2 | Usar la notebook como red Wi-Fi del robot | `./hotspot.sh --ligar` | 🧠 tú |
| 3 | Cambiar la Wi-Fi del robot a `ROBO-VIGIA` en su aplicación | — | 🧠 tú |
| 4 | Encontrar la dirección del robot | `./hotspot.sh --clientes` | ⚙️ script |
| 5 | Vigilar mientras el niño usa el robot (o en silencio, durante 10 min) | `sudo python3 vigia_robo.py --iface <placa> --ip <endereço> --saida relatorio.md` | ⚙️ script |
| 6 | Leer el informe: destinos, empresas, país de la empresa, envío minuto a minuto | abrir `relatorio.md` | 🧠 tú |
| 7 | Desactivar el hotspot | `./hotspot.sh --desligar` | ⚙️ script |

Consejo para probarlo: deja el robot **10 minutos encendido sin que nadie hable**. Si el gráfico minuto a minuto muestra un envío grande durante esos minutos, está enviando datos por su cuenta.

## Qué lee y qué no lee

- Lee **adónde** van los paquetes, **cuántos** datos se envían y los **nombres** que el robot consulta al DNS.
- **No** lee el contenido (la voz se envía cifrada). El vigía de red muestra el recorrido, no lo que se dijo.
- El país corresponde a la **empresa** propietaria del nombre, según la lista `dominios.json` (breve y fácil de corregir).
  Las direcciones sin nombre aparecen como «no identificado»: el robot usó una dirección fija.
- Los tamaños son aproximados (contenido de los paquetes, sin encabezados).

## Archivos

- `vigia_robo.py` — el vigía de red (`--iface` en vivo con sudo, `--pcap` para una captura grabada, `--stdin`).
- `hotspot.sh` — activa y desactiva la red `ROBO-VIGIA` mediante NetworkManager y muestra quién está conectado.
- `dominios.json` — nombre → empresa y país de la empresa.
- `exemplo/` — generador de captura **inventada** (direcciones reservadas para documentación) y su informe.
- `teste.sh` — 7 pruebas con el ejemplo.

## Estado

- ✅ Probado: lectura de capturas, nombres vía DNS, direcciones sin nombre, porcentajes, gráfico.
- 🔶 Falta probar en vivo: `hotspot.sh` y la captura con un robot real (lo haremos con Bean Bun).
