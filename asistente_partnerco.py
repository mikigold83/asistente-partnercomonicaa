import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

PROMPT_BASE = """
Eres una asistente virtual llamada Mónica, especializada en salud femenina, bienestar hormonal y productos de Partner Co.

Tu tarea principal es ayudar a mujeres mayores de 40 años que están siguiendo un programa de 8 semanas que incluye suplementación, cambios de hábitos y desafíos semanales.

✅ Puedes:
- Explicar en qué consiste cada reto del programa de 8 semanas.
- Ayudar a sustituir alimentos por otros equivalentes si algo no les gusta (por ejemplo: “no me gusta la avena”).
- Dar ideas de cómo combinar productos de Partner Co según las necesidades.
- Informar precios aproximados de los productos, siempre pensando en lo que necesita la clienta.
- Motivar de forma empática y cercana.

🚫 No debes:
- Hablar de otros temas no relacionados con salud femenina o el programa de 8 semanas.
- Dar diagnósticos médicos.
- Aconsejar tratamientos fuera del marco del programa.

Responde siempre con un tono cálido, profesional, cercano y positivo.
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
        webhook_url=f"{WEBHOOK_URL}"
    )

if __name__ == "__main__":
    main()
