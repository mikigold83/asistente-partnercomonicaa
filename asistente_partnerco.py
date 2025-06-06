import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

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

from openai import OpenAI

client = OpenAI(api_key=openai.api_key)

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": PROMPT_BASE},
                {"role": "user", "content": user_input}
            ]
        )
        answer = response.choices[0].message.content.strip()
        await update.message.reply_text(answer)
    except Exception as e:
        await update.message.reply_text("Lo siento, ha ocurrido un error. Por favor, intenta más tarde.")
        print(f"Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()

