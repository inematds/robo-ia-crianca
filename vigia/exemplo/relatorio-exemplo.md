> **Exemplo inventado** (exemplo/gerar_exemplo.py): endereços de documentação, não é medição de nenhum robô.

# Vigia do robô — relatório

- Robô: `10.42.0.50`
- Tempo observado: 5.7 min · 206 pacotes
- Enviado pelo robô para fora de casa: **151.7 KB** para 5 destino(s) (mais 141 B dentro da rede de casa)
- Para empresas da China (pela lista): **98%**
- Para destinos não identificados: 1% (veja a tabela)
- Nomes que o robô procurou: api.tenclass.net, ark.cn-beijing.volces.com, api.deepseek.com, pool.ntp.org

| Destino | Quem | País da empresa | Enviado | Recebido | Pacotes |
|---|---|---|---:|---:|---:|
| api.tenclass.net (203.0.113.10) | servidor público do XiaoZhi | China (provável) | 145.7 KB | 17.0 KB | 180 |
| ark.cn-beijing.volces.com (203.0.113.20) | ByteDance / Volcengine (Doubao) | China | 3.1 KB | 15.6 KB | 8 |
| 198.51.100.77 | não identificado (endereço fixo, sem perguntar o nome) | ? | 2.3 KB | 0 B | 8 |
| api.deepseek.com (203.0.113.30) | DeepSeek | China | 500 B | 0 B | 1 |
| 10.42.0.1 | rede local (roteador / DNS de casa) | casa | 141 B | 205 B | 8 |
| pool.ntp.org (198.51.100.5) | acerto do relógio (normal) | varia | 48 B | 0 B | 1 |

## Envio minuto a minuto
Se aparece envio em minutos em que ninguém falou com o robô, ele está mandando dados sozinho.

```
05:00  ███████████████ 31.0 KB
05:01  ██████████████████████████████ 60.8 KB
05:02  █████ 10.8 KB
05:03  █ 1.3 KB
05:04  ███████████████████████ 47.1 KB
05:05  █ 900 B
```

Tamanhos aproximados (conteúdo dos pacotes, sem cabeçalhos). Lista de nomes: dominios.json. Guia: https://inematds.github.io/robo-ia-crianca/guia/
