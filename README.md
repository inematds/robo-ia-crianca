# Robô de IA para criança: o que você precisa saber antes de comprar

[![Robô de IA para criança](guia/assets/banner.jpg)](https://inematds.github.io/robo-ia-crianca/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

Este guia explica os robôs de IA baratos para criança que aparecem nos marketplaces brasileiros. Eles não têm inteligência dentro: gravam a voz (e, em alguns modelos, a imagem) e mandam pela internet para serviços de IA na China, que respondem em voz. Aqui você vê os riscos, um checklist para usar antes de comprar, os cuidados se já comprou, um **kit do educador** (aula de 30 min com cartaz, atividade e bilhete), um **vigia de rede** que mostra com quem o robô conversa e um caminho, ainda a testar, para que o "cérebro" rode no seu próprio computador. O **controle dos pais** (histórico, horário, filtro, alerta) está no [roadmap](ROADMAP.md). Não precisa saber nada de tecnologia: é só ler.

## 📖 Guia

Guia completo (landing + passo a passo): **https://inematds.github.io/robo-ia-crianca/guia/**

🎬 Vídeo: https://www.youtube.com/shorts/2td4u5iq3MU

## O que tem no repositório

| Arquivo | Para quê |
|---|---|
| [`guia/`](guia/) | O guia em PT, EN e ES (GitHub Pages) |
| [`docs/checklist.md`](docs/checklist.md) | Checklist para imprimir: antes de comprar e se já comprou |
| [`docs/cerebro-local.md`](docs/cerebro-local.md) | Roteiro técnico **a testar** para rodar o cérebro do robô em casa |
| [`kit-educador/`](kit-educador/) | Aula de 30 min para 6–12 anos + [folhas para imprimir](https://inematds.github.io/robo-ia-crianca/kit-educador/imprimir.html) (PT/EN/ES) |
| [`vigia/`](vigia/) | Vigia de rede: com quem o robô conversa e quanto manda (`./teste.sh` roda sem robô) |
| [`ROADMAP.md`](ROADMAP.md) | Etapas e o controle dos pais planejado |
| [`capa/capa.png`](capa/capa.png) | Capa do catálogo INEMA |

## O processo, do início ao fim

Quem faz: 🧠 sessão com o Nei · ⚙️ script/timer · 🤖 `claude -p`

1. 🧠 **Levantamento** — anúncios de robôs de IA infantis num marketplace brasileiro, pesquisas públicas sobre brinquedos de IA e projetos abertos (xiaozhi-esp32-server, OpenToys). Separar o que é confirmado do que é provável.
2. ⚙️ **Capa e hero** — `node ~/.claude/skills/capa-inema/assets/gerar-capa.cjs --repo . --title "Robô de IA para criança" --cat "Segurança" --gerador auto --save-raw guia/assets/hero.png` (Codex image_gen; flux2-klein só se falhar).
3. ⚙️ **Banners** — `bash ~/.claude/skills/projetos-landing-guia/assets/gerar-banner.sh` nos estilos `live` e `grade`, em PT, EN e ES (6 imagens em `guia/assets/`). Conferir o texto de cada uma.
4. 🧠 **Guia PT** — `guia/index.html`, a partir do template da skill `projetos-landing-guia`.
5. ⚙️ **Tradução** — `guia/en/` e `guia/es/` e os READMEs pelo tradutor central: `cat pedido.txt | ~/projetos/wifi/scripts/inema-traduz`.
6. 🧠 **Docs** — `docs/checklist.md` e `docs/cerebro-local.md`.
7. 🤖 **Revisor independente** — agente novo lê o guia com a lista fixa da skill.
8. 🧠 **Publicar** — `git push`; o GitHub Actions (`.github/workflows/pages.yml`) publica o Pages. Conferir `/guia/`, `/guia/en/`, `/guia/es/` com HTTP 200.
9. 🧠 **Kit do educador** — `kit-educador/aula.md` + `kit-educador/imprimir.html` (cartaz, atividade, bilhete); EN/ES em `kit-educador/en/` e `es/` pelo tradutor central.
10. ⚙️ **Vigia de rede** — `cd vigia && ./teste.sh` (7 testes com captura inventada); ao vivo: `./hotspot.sh --ligar` → `sudo python3 vigia_robo.py --iface <placa> --ip <robô>`.
11. 🧠 **Teste do cérebro em casa** (pendente) — comprar um Bean Bun, abrir, seguir `docs/cerebro-local.md` e atualizar guia + docs com o resultado.
12. 🧠 **Controle dos pais** (planejado) — ver [`ROADMAP.md`](ROADMAP.md); depende do passo 11.
13. 🧠 **Portal e Telegram** — feitos fora deste repo (portal inema.club, tópico INEMA.ROBOT).

## Aviso

Conteúdo educativo do INEMA. Não citamos marcas de vendedores nem links de anúncios. O caminho "cérebro em casa" ainda não foi testado pelo INEMA.

---
[INEMA.CLUB](https://inema.club)
