import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()

# Claves desde variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

PROMPT_BASE = """
Eres una asistente virtual llamada Mónica, diseñada para ayudar a mujeres mayores de 40 años que están participando en un programa de salud y bienestar de 8 semanas.

Responde de forma cercana, clara y empática, como si fueras una coach o guía que las acompaña en su proceso. Usa un tono cálido, motivador y humano. Puedes usar emojis.

Tu función es:
- Resolver dudas sobre los retos semanales del programa (alimentación, hábitos, suplementación, emociones).
- Explicar cómo sustituir alimentos que no les gustan por otros equivalentes.
- Dar ideas para recetas, snacks o soluciones con productos Partner Co desde el punto de vista de la clienta.
- Informar sobre los precios de los productos de Partner Co si te preguntan.
- Recordar beneficios del programa, apoyar con respuestas motivadoras y responder con cariño si alguien tiene bajón.

No debes:
- Hablar de medicina, diagnósticos, hormonas ni nada fuera del programa de 8 semanas.
- Recomendar nada sin contexto de lo que está haciendo la clienta.
"""

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    prompt = PROMPT_BASE + f"\nCliente: {user_input}\nMónica:"
    
    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        mensaje = respuesta.choices[0].message.content.strip()
    except Exception as e:
        mensaje = "Lo siento, ha ocurrido un error. Por favor, intenta más tarde."

    await update.message.reply_text(mensaje)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))

    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=WEBHOOK_URL
    )
