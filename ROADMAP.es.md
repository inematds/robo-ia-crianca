# Hoja de ruta — robo-ia-crianca

| Etapa | Qué ofrece | Estado |
|---|---|---|
| 1. Guía + lista de verificación | Qué revisar antes de comprar y cuidados para quienes ya compraron (PT/EN/ES) | ✅ listo (07/11/2026) |
| 2. Kit del educador | Clase de 30 min, cartel, actividad y nota para las familias | ✅ listo (07/11/2026) |
| 3. Vigía de red | Muestra con quién se comunica el robot y cuántos datos envía, minuto a minuto | ✅ probado con una captura de ejemplo · 🔶 falta probarlo en vivo con un robot |
| 4. Cerebro en casa | Robot reprogramado para comunicarse con un servidor familiar, en español, sin nube | 🔶 guion escrito (`docs/cerebro-local.md`), falta probar |
| 5. **Control parental** | Panel en el servidor de casa (abajo) | 📋 planificado — depende de la etapa 4 |

## Etapa 5 — Control parental (planificado)

Solo tiene sentido con el cerebro en casa: cuando la conversación pasa por el servidor familiar, los padres
pueden controlarla. En un robot conectado a la nube del fabricante, nada de esto es posible.

| Recurso | Cómo | Para qué |
|---|---|---|
| **Historial de conversaciones** | El servidor guarda el texto de cada pregunta y respuesta, solo en la computadora de casa | Los padres leen lo que conversó el niño |
| **Horario permitido** | Fuera del horario, el servidor responde «ahora es hora de descansar» | Evitar que el robot se convierta en compañía de madrugada |
| **Límite de tiempo por día** | Contador de minutos de conversación por día | El mismo control que ya existe para el tiempo frente a la pantalla |
| **Filtro de temas** | Instrucción fija en el modelo local + lista de temas bloqueados; ante un tema bloqueado, responde «pregúntale a un adulto» | Respuestas adecuadas a la edad |
| **Alerta para los padres** | Una palabra de alerta (dirección, contraseña, «secreto», tristeza repetida) genera un aviso en el celular de los padres | Saberlo de inmediato, sin leer todo |
| **Botón para apagar** | Página en el celular de los padres que apaga el cerebro con un toque | Corte inmediato, sin abrir el robot |
| **Informe semanal** | Resumen: tiempo de uso, temas más frecuentes, alertas | Conversación en familia al final de la semana |
| **Borrar todo** | Un botón borra el historial | Los datos son de la familia |

Orden previsto: historial y horario primero (más sencillos), luego límite, filtro, alerta,
botón e informe. Todo en español, todo local, con la misma regla que el resto del proyecto:
**nada sale de casa**.

### Antes de empezar la etapa 5

1. Comprar un Bean Bun (o un robot ESP32-S3 parecido), abrirlo y confirmar la placa.
2. Hacer funcionar la etapa 4 con la red bloqueada.
3. Medir con el vigía (etapa 3) que, después del cambio, no salga nada al exterior.
4. Solo entonces armar el panel, empezando por el historial.
