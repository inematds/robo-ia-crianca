#!/usr/bin/env bash
# Teste do vigia com a captura inventada do exemplo (não precisa de robô nem de sudo).
set -euo pipefail
cd "$(dirname "$0")"
python3 exemplo/gerar_exemplo.py >/dev/null
SAIDA=$(python3 vigia_robo.py --pcap exemplo/exemplo.pcap --ip 10.42.0.50 2>/dev/null)
falha() { echo "FALHOU: $1"; exit 1; }
grep -q "api.tenclass.net (203.0.113.10) | servidor público do XiaoZhi" <<<"$SAIDA" || falha "nome via DNS"
grep -q "ark.cn-beijing.volces.com (203.0.113.20) | ByteDance" <<<"$SAIDA" || falha "Doubao"
grep -q "198.51.100.77 | não identificado (endereço fixo" <<<"$SAIDA" || falha "endereço sem nome"
grep -q "Para empresas da China (pela lista): \*\*98%\*\*" <<<"$SAIDA" || falha "porcentagem China"
grep -q "Tempo observado: 5.7 min · 206 pacotes" <<<"$SAIDA" || falha "contagem"
[ "$(grep -c '█' <<<"$SAIDA")" -eq 6 ] || falha "6 minutos no gráfico"
# robô errado: não pode inventar nada
python3 vigia_robo.py --pcap exemplo/exemplo.pcap --ip 10.42.0.99 2>/dev/null | grep -q "Nenhum pacote" || falha "ip sem tráfego"
{ echo "> **Exemplo inventado** (exemplo/gerar_exemplo.py): endereços de documentação, não é medição de nenhum robô."; echo; echo "$SAIDA"; } > exemplo/relatorio-exemplo.md
echo "OK: vigia passou nos 7 testes"
