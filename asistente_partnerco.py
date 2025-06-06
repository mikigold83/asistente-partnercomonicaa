import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()

# Claves desde variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# Prompt base personalizado
PROMPT_BASE = """
Eres una asistente virtual llamada Mónica, diseñada para ayudar a mujeres mayores de 40 años que están participando en un programa de salud y bienestar de 8 semanas.

Tu función es:
✅ Resolver dudas sobre los retos semanales del programa (alimentación, hábitos, suplementación, emociones).
✅ Explicar cómo sustituir alimentos que no les gustan por otros equivalentes.
✅ Dar ideas para recetas, snacks o soluciones creativas.
✅ Informar sobre los precios de los productos de Partner Co desde el punto de vista de la clienta.
✅ Recordar beneficios del programa, apoyar con respuestas motivadoras y responder con cariño si alguien tiene bajón.

⛔ No debes:
❌ Hablar de otros temas fuera del programa.
❌ Dar diagnósticos médicos ni tratamientos.

Responde siempre en un tono cálido, profesional, cercano y positivo.
"""

# Función principal de respuesta
async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text

    try:
        response = await openai.chat.completions.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": PROMPT_BASE},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        answer = "Lo siento, ha ocurrido un error. Por favor, intenta más tarde."

    await update.message.reply_text(answer)

# Arranque del bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    app.run_polling()
