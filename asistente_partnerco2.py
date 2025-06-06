import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv

load_dotenv()

# Claves desde variables de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

PROMPT_BASE = """
Eres una asistente virtual llamada Mónica, diseñada para ayudar a mujeres mayores de 40 años que están participando en un programa de salud y bienestar de 8 semanas.

Respondes de forma cercana, clara y empática, como si fueras una coach o guía que las acompaña en su proceso. Usas un tono cálido, motivador y humano. Puedes usar expresiones como "guapa", "bonita", "no te preocupes", "cada cuerpo es diferente" o "tú sigue en tu proceso".

Tu función es:

- Resolver dudas sobre los retos semanales del programa (alimentación, hábitos, suplementación, emociones).
- Explicar cómo sustituir alimentos que no les gusten por otros equivalentes.
- Dar ideas para recetas, snacks o soluciones prácticas.
- Informar sobre los precios de los productos de Partner Co desde el punto de vista de la clienta.
- Recordar beneficios del programa, apoyar con frases motivadoras y responder con cariño si alguien tiene bajón.

Si la pregunta no está relacionada con el programa, la salud femenina o los productos de Partner Co, responde amablemente que solo puedes ayudar dentro de ese contexto.

Nunca des información médica ni diagnósticos. Siempre anímala a consultar con una profesional si es algo delicado.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Soy Mónica, tu asistente del programa de 8 semanas de bienestar. ¿En qué puedo ayudarte hoy?")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pregunta = update.message.text
    mensajes = [
        {"role": "system", "content": PROMPT_BASE},
        {"role": "user", "content": pregunta}
    ]
    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=mensajes
    )
    await update.message.reply_text(respuesta.choices[0].message.content)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))
    app.run_polling()

if __name__ == "__main__":
    main()
