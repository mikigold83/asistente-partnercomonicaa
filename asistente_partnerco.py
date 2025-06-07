import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

PROMPT_BASE = """
Eres una asistente virtual llamada Mónica, especializada en salud femenina, bienestar hormonal y productos de Partner Co.

Tu tarea principal es ayudar a mujeres mayores de 40 años que están siguiendo un programa de 8 semanas que incluye suplementación, cambios de hábitos y desafíos semanales.

Responde con un tono cálido, profesional, cercano y positivo.
"""

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    messages = [
        {"role": "system", "content": PROMPT_BASE},
        {"role": "user", "content": user_input}
    ]
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages
        )
        response = completion.choices[0].message.content
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text("Lo siento, ha ocurrido un error. Por favor, intenta más tarde.")
        print(f"Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    # IMPORTANTE: aquí defines el webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=os.environ.get("WEBHOOK_URL")  # la definiremos en Render
    )
