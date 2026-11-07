# Robô de IA para criança: o que você precisa saber antes de comprar

[![Robô de IA para criança](guia/assets/banner.jpg)](https://inematds.github.io/robo-ia-crianca/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

Este guia explica os robôs de IA baratos para criança que aparecem nos marketplaces brasileiros. Eles não têm inteligência dentro: gravam a voz (e, em alguns modelos, a imagem) e mandam pela internet para serviços de IA na China, que respondem em voz. Aqui você vê os riscos, um checklist para usar antes de comprar, os cuidados se já comprou e um caminho, ainda a testar, para que o "cérebro" rode no seu próprio computador. Não precisa saber nada de tecnologia: é só ler.

## 📖 Guia

Guia completo (landing + passo a passo): **https://inematds.github.io/robo-ia-crianca/guia/**

## O que tem no repositório

| Arquivo | Para quê |
|---|---|
| [`guia/`](guia/) | O guia em PT, EN e ES (GitHub Pages) |
| [`docs/checklist.md`](docs/checklist.md) | Checklist para imprimir: antes de comprar e se já comprou |
| [`docs/cerebro-local.md`](docs/cerebro-local.md) | Roteiro técnico **a testar** para rodar o cérebro do robô em casa |
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
9. 🧠 **Teste do cérebro em casa** (pendente) — comprar um Bean Bun, abrir, seguir `docs/cerebro-local.md` e atualizar guia + docs com o resultado.
10. 🧠 **Portal e Telegram** — feitos pelo Nei, fora deste repo.

## Aviso

Conteúdo educativo do INEMA. Não citamos marcas de vendedores nem links de anúncios. O caminho "cérebro em casa" ainda não foi testado pelo INEMA.

---
[INEMA.CLUB](https://inema.club)
