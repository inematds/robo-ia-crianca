# Roadmap — robo-ia-crianca

| Etapa | O que entrega | Estado |
|---|---|---|
| 1. Guia + checklist | O que olhar antes de comprar e cuidados para quem já comprou (PT/EN/ES) | ✅ pronto (07/11/2026) |
| 2. Kit do educador | Aula de 30 min, cartaz, atividade e bilhete para os pais | ✅ pronto (07/11/2026) |
| 3. Vigia de rede | Mostra com quem o robô conversa e quanto manda, minuto a minuto | ✅ testado com captura de exemplo · 🔶 falta testar ao vivo com um robô |
| 4. Cérebro em casa | Robô regravado falando com um servidor da família, em português, sem nuvem | 🔶 roteiro escrito (`docs/cerebro-local.md`), falta testar |
| 5. **Controle dos pais** | Painel no servidor de casa (abaixo) | 📋 planejado — depende da etapa 4 |

## Etapa 5 — Controle dos pais (planejado)

Só faz sentido com o cérebro em casa: quando a conversa passa pelo servidor da família, os pais
passam a mandar nela. Num robô ligado à nuvem do fabricante, nada disto é possível.

| Recurso | Como | Para quê |
|---|---|---|
| **Histórico das conversas** | O servidor guarda o texto de cada pergunta e resposta, só no computador de casa | Os pais leem o que a criança conversou |
| **Horário permitido** | Fora do horário o servidor responde "agora é hora de descansar" | Robô não vira companhia da madrugada |
| **Limite de tempo por dia** | Contador de minutos de conversa por dia | Mesmo controle que já existe para tela |
| **Filtro de assunto** | Instrução fixa no modelo local + lista de temas bloqueados; tema bloqueado vira "pergunte a um adulto" | Respostas adequadas à idade |
| **Alerta para os pais** | Palavra de alerta (endereço, senha, "segredo", tristeza repetida) gera aviso no celular dos pais | Saber na hora, sem ler tudo |
| **Botão de desligar** | Página no celular dos pais que desliga o cérebro com um toque | Corte imediato, sem abrir o robô |
| **Relatório da semana** | Resumo: tempo de uso, assuntos mais falados, alertas | Conversa em família no fim de semana |
| **Apagar tudo** | Um botão apaga o histórico | O dado é da família |

Ordem prevista: histórico e horário primeiro (mais simples), depois limite, filtro, alerta,
botão, relatório. Tudo em português, tudo local, com a mesma regra do resto do projeto:
**nada sai de casa**.

### Antes de começar a etapa 5

1. Comprar um Bean Bun (ou robô ESP32-S3 parecido), abrir e confirmar a placa.
2. Fazer a etapa 4 funcionar com a rede bloqueada.
3. Medir com o vigia (etapa 3) que, depois da troca, nada sai para fora.
4. Só então montar o painel, começando pelo histórico.
