# Roadmap — robo-ia-crianca

| Stage | What it delivers | Status |
|---|---|---|
| 1. Guide + checklist | What to check before buying and how to care for a robot you already bought (PT/EN/ES) | ✅ ready (07/11/2026) |
| 2. Educator's kit | 30-minute lesson, poster, activity, and note to parents | ✅ ready (07/11/2026) |
| 3. Network monitor | Shows who the robot talks to and how much it sends, minute by minute | ✅ tested with a sample capture · 🔶 still needs a live test with a robot |
| 4. Brain at home | A reprogrammed robot that talks to a family server in Portuguese, with no cloud | 🔶 guide written (`docs/cerebro-local.md`), still needs testing |
| 5. **Parental controls** | Dashboard on the home server (below) | 📋 planned — depends on stage 4 |

## Stage 5 — Parental controls (planned)

This only makes sense with the brain at home: when conversations go through the family server, parents can manage them. None of this is possible with a robot connected to the manufacturer's cloud.

| Feature | How | Why |
|---|---|---|
| **Conversation history** | The server stores the text of each question and answer, only on the home computer | Parents can read what the child talked about |
| **Allowed hours** | Outside allowed hours, the server replies, "It's time to rest now" | The robot won't become a late-night companion |
| **Daily time limit** | A counter tracks conversation minutes per day | The same kind of limit already used for screen time |
| **Topic filter** | A fixed instruction in the local model plus a list of blocked topics; a blocked topic gets the reply, "Ask an adult" | Age-appropriate answers |
| **Alert for parents** | An alert word or phrase (address, password, “secret,” repeated sadness) sends a notification to the parents' phone | Know right away without reading everything |
| **Power-off button** | A page on the parents' phone that turns off the brain with one tap | Shut it down right away without opening the robot |
| **Weekly report** | Summary of usage time, most discussed topics, and alerts | A family conversation over the weekend |
| **Delete everything** | One button deletes the history | The data belongs to the family |

Planned order: history and allowed hours first (simplest), then time limit, filter, alert,
button, and report. Everything in Portuguese, everything local, with the same rule as the rest of the project:
**nothing leaves home**.

### Before starting stage 5

1. Buy a Bean Bun (or a similar ESP32-S3 robot), open it, and confirm the board.
2. Get stage 4 working with the network blocked.
3. Use the network monitor (stage 3) to confirm that nothing leaves the network after the change.
4. Only then build the dashboard, starting with conversation history.
