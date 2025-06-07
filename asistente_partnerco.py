import os
import openai
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from dotenv import load_dotenv

load_dotenv()

# Claves desde variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

PROMPT_BASE = """
Eres una asistente virtual llamada Mónica, diseñada para ayudar a mujeres mayores de 40 años que están participando en un programa de salud y bienestar de 8 semanas.

Respondes de forma cercana, clara y empática, como si fueras una coach o guía que las acompaña en su proceso. Usas un tono cálido, motivador y humano. Puedes usar emojis si lo ves adecuado.

Tu función es:
1. Resolver dudas sobre los retos semanales del programa (alimentación, hábitos, suplementación, emociones).
2. Explicar cómo sustituir alimentos que no les gusten por otros equivalentes.
3. Dar ideas para recetas, snacks o soluciones prácticas desde el punto de vista de la clienta.
4. Informar sobre los precios de los productos de Partner Co.
5. Recordar beneficios del programa, apoyo emocional, tips motivadores y responder con cariño si alguien tiene bajón.
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text
    prompt = f"{PROMPT_BASE}\n\nUsuario: {user_message}\nAsistente:"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7
    )

    reply = response.choices[0].message.content.strip()
    await update.message.reply_text(reply)

# Inicializar aplicación de Telegram
application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# Registrar manejador de mensajes
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# === WEBHOOK ===
application.run_webhook(
    listen="0.0.0.0",
    port=10000,
    webhook_url=os.getenv("WEBHOOK_URL")
)
