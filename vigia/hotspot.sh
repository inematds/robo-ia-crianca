#!/usr/bin/env bash
# Hotspot do vigia: o computador vira a rede Wi-Fi do robô, para enxergar o tráfego dele.
# Linux com NetworkManager (Ubuntu, Mint, Fedora). O notebook precisa de internet POR CABO
# (ou de uma 2ª placa Wi-Fi): a placa Wi-Fi vira a rede do robô e deixa de ser a internet.
#
#   ./hotspot.sh --ligar  [placa]   cria a rede "ROBO-VIGIA" (senha abaixo)
#   ./hotspot.sh --clientes [placa] mostra quem está ligado (o robô aparece aqui)
#   ./hotspot.sh --desligar         desliga a rede
set -euo pipefail

REDE="ROBO-VIGIA"
SENHA="${SENHA_HOTSPOT:-$(od -An -N6 -tx1 /dev/urandom | tr -d ' \n')}"  # aleatória se não vier SENHA_HOTSPOT

placa_wifi() {
  nmcli -t -f DEVICE,TYPE device | awk -F: '$2=="wifi"{print $1; exit}'
}

case "${1:-}" in
  --ligar)
    PLACA="${2:-$(placa_wifi)}"
    [ -n "$PLACA" ] || { echo "Nenhuma placa Wi-Fi encontrada."; exit 1; }
    if ! nmcli -t -f DEVICE,TYPE,STATE device | grep -v "^$PLACA:" | grep -Eq ':(ethernet|wifi):connected$'; then
      echo "Atenção: fora a placa $PLACA, nada está conectado. Ligue o cabo de rede antes,"
      echo "senão o robô fica sem internet e o relatório sai vazio. (Ctrl+C para parar, Enter segue)"
      read -r _
    fi
    nmcli device wifi hotspot ifname "$PLACA" con-name robo-vigia ssid "$REDE" password "$SENHA"
    echo
    echo "Rede \"$REDE\" ligada na placa $PLACA (senha: $SENHA)."
    echo "1. No app do robô, troque a Wi-Fi dele para \"$REDE\"."
    echo "2. Rode: ./hotspot.sh --clientes $PLACA   (anote o endereço do robô, ex.: 10.42.0.50)"
    echo "3. Rode: sudo python3 vigia_robo.py --iface $PLACA --ip <endereço> --saida relatorio.md"
    ;;
  --clientes)
    PLACA="${2:-$(placa_wifi)}"
    echo "Aparelhos ligados em $PLACA:"
    ip neigh show dev "$PLACA" | awk '$1 !~ /:/ {print "  " $1 "  (" $3 ")"}'
    LEASES=$(ls /var/lib/NetworkManager/dnsmasq-"$PLACA".leases 2>/dev/null || true)
    if [ -n "$LEASES" ]; then
      echo "Nomes informados pelos aparelhos:"
      awk '{print "  " $3 "  " $4}' "$LEASES"
    fi
    ;;
  --desligar)
    nmcli connection down robo-vigia && nmcli connection delete robo-vigia
    echo "Hotspot desligado."
    ;;
  *)
    sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//'
    ;;
esac
