# AI Robot for Kids: What to Know Before You Buy

[![AI Robot for Kids](guia/assets/banner.jpg)](https://inematds.github.io/robo-ia-crianca/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

This guide explains the low-cost AI robots for kids sold on Brazilian marketplaces. They don’t have intelligence built in: they record voice (and, in some models, images) and send it over the internet to AI services in China, which reply by voice. Here you’ll find the risks, a checklist to use before buying, precautions to take if you’ve already bought one, an **educator’s kit** (a 30-minute lesson with a poster, activity, and note to parents), a **network monitor** that shows who the robot talks to, and an approach, still to be tested, for running the “brain” on your own computer. **Parental controls** (history, schedule, filters, alerts) are on the [roadmap](ROADMAP.en.md). You don’t need to know anything about technology: just read.

## 📖 Guide

Complete guide (landing page + step-by-step instructions): **https://inematds.github.io/robo-ia-crianca/guia/en/**

## What’s in the repository

| File | What it’s for |
|---|---|
| [`guia/`](guia/) | The guide in PT, EN, and ES (GitHub Pages) |
| [`docs/checklist.md`](docs/checklist.md) | Printable checklist: before buying and if you’ve already bought one |
| [`docs/cerebro-local.md`](docs/cerebro-local.md) | Technical guide **to be tested** for running the robot’s brain at home |
| [`kit-educador/en/`](kit-educador/en/) | 30-minute lesson for ages 6–12 + [printable sheets](https://inematds.github.io/robo-ia-crianca/kit-educador/en/imprimir.html) (PT/EN/ES) |
| [`vigia/`](vigia/) | Network monitor: who the robot talks to and how much it sends (`./teste.sh` runs without a robot) |
| [`ROADMAP.md`](ROADMAP.en.md) | Planned stages and parental controls |
| [`capa/capa.png`](capa/capa.png) | INEMA catalog cover |

## The process, from start to finish

Who does what: 🧠 session with Nei · ⚙️ script/timer · 🤖 `claude -p`

1. 🧠 **Research** — Listings for children’s AI robots on a Brazilian marketplace, public research on AI toys, and open-source projects (xiaozhi-esp32-server, OpenToys). Separate what is confirmed from what is likely.
2. ⚙️ **Cover and hero image** — `node ~/.claude/skills/capa-inema/assets/gerar-capa.cjs --repo . --title "Robô de IA para criança" --cat "Segurança" --gerador auto --save-raw guia/assets/hero.png` (Codex image_gen; flux2-klein only if it fails).
3. ⚙️ **Banners** — `bash ~/.claude/skills/projetos-landing-guia/assets/gerar-banner.sh` in the `live` and `grade` styles, in PT, EN, and ES (6 images in `guia/assets/`). Check the text in each one.
4. 🧠 **Guide in Portuguese** — `guia/index.html`, based on the `projetos-landing-guia` skill template.
5. ⚙️ **Translation** — `guia/en/` and `guia/es/`, and the READMEs, using the central translator: `cat pedido.txt | ~/projetos/wifi/scripts/inema-traduz`.
6. 🧠 **Docs** — `docs/checklist.md` and `docs/cerebro-local.md`.
7. 🤖 **Independent reviewer** — a new agent reads the guide using the skill’s fixed checklist.
8. 🧠 **Publish** — `git push`; GitHub Actions (`.github/workflows/pages.yml`) publishes GitHub Pages. Check `/guia/`, `/guia/en/`, `/guia/es/` for HTTP 200.
9. 🧠 **Educator’s kit** — `kit-educador/aula.md` + `kit-educador/imprimir.html` (poster, activity, note to parents); EN/ES in `kit-educador/en/` and `es/` using the central translator.
10. ⚙️ **Network monitor** — `cd vigia && ./teste.sh` (7 tests with fabricated captures); live use: `./hotspot.sh --ligar` → `sudo python3 vigia_robo.py --iface <placa> --ip <robô>`.
11. 🧠 **Test the at-home brain** (pending) — buy a Bean Bun, open it, follow `docs/cerebro-local.md`, and update the guide + docs with the results.
12. 🧠 **Parental controls** (planned) — see [`ROADMAP.md`](ROADMAP.en.md); depends on step 11.
13. 🧠 **Portal and Telegram** — handled outside this repository (inema.club portal, INEMA.ROBOT topic).

## Notice

Educational content from INEMA. We don’t name seller brands or link to listings. INEMA has not yet tested the “brain at home” approach.

---
[INEMA.CLUB](https://inema.club)
