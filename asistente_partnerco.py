import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()

# Variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

PROMPT_BASE = """
Eres una asistente virtual llamada Mónica, diseñada para ayudar a mujeres mayores de 40 años que están participando en un programa de salud y bienestar de 8 semanas.

Respondes de forma cercana, clara y empática, como si fueras una coach o guía que las acompaña en su proceso. Usas un tono cálido, motivador y humano. Puedes usar emojis si es necesario.

Tu función es:
- Resolver dudas sobre los retos semanales del programa (alimentación, hábitos, suplementación, emociones).
- Explicar cómo sustituir alimentos que no les gusten por otros equivalentes.
- Dar ideas para recetas, snacks o soluciones prácticas.
- Informar sobre los precios de los productos de Partner Co desde el punto de vista de la clienta.
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": PROMPT_BASE},
            {"role": "user", "content": user_input}
        ]
    )

    reply = response['choices'][0]['message']['content']
    await update.message.reply_text(reply)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hola, soy Mónica. ¿En qué puedo ayudarte?")

def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=os.getenv("WEBHOOK_URL")
    )

if __name__ == "__main__":
    main()
