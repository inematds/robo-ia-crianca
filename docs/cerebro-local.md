# Cérebro em casa — roteiro técnico a testar

> **Status: roteiro a testar.** O INEMA ainda não testou este caminho. Vamos comprar um
> robô "Bean Bun" para abrir e testar; este documento será atualizado com o resultado.
> Abrir e regravar o aparelho pode estragá-lo e acaba com a garantia.

## Objetivo

Manter o corpo barato do robô (microfone, alto-falante, olhos) e trocar o "cérebro" da nuvem
chinesa por um servidor que roda num computador da sua casa. Resultado esperado: o robô fala
português e nenhum áudio ou imagem sai da sua rede.

## O que sabemos e o que é hipótese

| Item | Status |
|---|---|
| A placa dos robôs é ESP32-S3 com o ecossistema XiaoZhi | **Provável** — só confirma abrindo |
| Placas desse tipo são vendidas avulsas por US$ 8–18 | Confirmado (ex.: [SpotPear AI-BOX](https://spotpear.com/shop/ESP32-S3-AI-BOX-deepseek-xiaozhi-doubao-0.71inch-LCD-Electronic-Eye-Toy-Doll-Robot/AI-BOX.html)) |
| Existe servidor aberto para hospedar em casa | Confirmado: [xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server), licença MIT |
| O servidor aceita LLM local (Ollama), voz local (FunASR, Sherpa) e vários TTS | Confirmado no README do projeto |
| O servidor tem README e painel em português do Brasil | Confirmado no README do projeto |
| Firmware aberto do ecossistema | [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) (licença MIT) |
| O firmware do robô comprado aceita ser regravado | **Não sabemos** — a testar |

## Peças

- **Servidor:** [xinnan-tech/xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server).
  Recomenda PC de 4 núcleos e 8 GB de memória. Tem instalação por Docker ou pelo código-fonte
  (ver `docs/Deployment.md` do projeto). Há README em português em `docs/readme/README_pt_BR.md`.
- **Firmware da placa:** [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32).
- **Alternativa:** [akdeb/OpenToys](https://github.com/akdeb/OpenToys) — ESP32-S3 + Whisper e
  modelos rodando no computador (foco em Mac com chip Apple), licença MIT, lista português entre os idiomas.

## Roteiro

1. **Abrir o robô e confirmar a placa.** Procurar "ESP32-S3" no chip. Fotografar a placa, o
   conector USB e os pontos de gravação. Se não for ESP32-S3, parar aqui.
2. **Montar o servidor em casa.**
   ```bash
   git clone https://github.com/xinnan-tech/xiaozhi-esp32-server.git
   # siga docs/Deployment.md (modo "最简化安装" = instalação mínima, sem banco de dados)
   ```
   Atenção: a configuração "gratuita" sugerida pelo projeto usa serviços de nuvem para o modelo
   (glm-4-flash) e para a voz (EdgeTTS). Para nada sair de casa, troque cada peça:
   - voz → texto: FunASR local (ou Sherpa / Whisper);
   - modelo de linguagem: Ollama, com um modelo que responda bem em português;
   - texto → voz: um TTS local com voz em português.
   Não use o servidor público de teste citado no README do projeto: ele recebe o áudio de quem conecta.
3. **Regravar o firmware** com o firmware XiaoZhi configurado para o endereço do seu servidor
   (OTA e WebSocket do servidor de casa), em vez do servidor do fabricante.
   ```bash
   git clone https://github.com/78/xiaozhi-esp32.git
   ```
   Antes de gravar, tentar fazer cópia do firmware original da placa, para poder voltar atrás.
4. **Testar com a internet bloqueada.** No roteador, bloquear a saída do robô para a internet,
   deixando só a rede local. Se ele continuar respondendo em português, o cérebro está em casa.
5. **Registrar o resultado** neste documento e no guia (o que funcionou, o que não funcionou, fotos).

## O que vamos medir no teste

- A placa é mesmo ESP32-S3 / XiaoZhi?
- Dá para regravar sem abrir solda?
- Tempo de resposta com tudo local.
- Qualidade da fala em português (entender e responder).
- O robô tenta acessar algum endereço de fora mesmo com o servidor local?

---
Guia: https://inematds.github.io/robo-ia-crianca/guia/ · INEMA.CLUB · https://inema.club
