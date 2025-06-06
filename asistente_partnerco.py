
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import os

# Claves desde variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

PROMPT_BASE = """
Eres una asistente virtual llamada Clara, especializada en salud femenina, bienestar hormonal y productos de Partner Co. 
Respondes de manera cercana, clara y profesional a mujeres mayores de 40 años que tienen dudas sobre menopausia, suplementación y cambios hormonales. 
Usas un lenguaje cálido y empático. 
Si la pregunta no está relacionada con estos temas, amablemente indicas que solo puedes ayudar en temas de salud femenina y productos de Partner Co.
"""

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": PROMPT_BASE},
            {"role": "user", "content": user_input}
        ]
    )
    answer = response.choices[0].message.content.strip()
    await update.message.reply_text(answer)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    print("🤖 Bot funcionando. Esperando mensajes...")
    app.run_polling()
