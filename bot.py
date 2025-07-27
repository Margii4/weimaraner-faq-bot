import os
import asyncio
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.enums import ParseMode
from dotenv import load_dotenv
from loguru import logger
from rag_utils import load_faq_docs_docx, split_docs, build_vector_store, get_vector_store

import openai

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGUAGES = {"English": "en", "Italiano": "it"}
DEFAULT_LANG = "en"

user_lang = {}
history_file = "user_history.json"
MAX_HISTORY = 5

def load_user_history():
    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_user_history(history):
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

user_history = load_user_history()

kb = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Resents"), KeyboardButton(text="Clear memory")],
    [KeyboardButton(text="English"), KeyboardButton(text="Italiano")]
], resize_keyboard=True)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

openai_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = {
    "en": (
        "You are an expert in the Weimaraner breed. "
        "Answer ONLY questions related to Weimaraners, using ONLY the facts provided in the context. "
        "If the question is off-topic or there isn't enough context, just say you don't know. "
        "Assume any follow-up question is still about the Weimaraner unless the user explicitly changes the breed or topic."
    ),
    "it": (
        "Sei un esperto della razza Weimaraner. "
        "Rispondi SOLO a domande relative ai Weimaraner, utilizzando SOLO i fatti forniti nel contesto. "
        "Se la domanda non è pertinente o non c'è abbastanza contesto, scrivi semplicemente che non lo sai. "
        "Considera ogni domanda successiva come riferita ancora ai Weimaraner, a meno che l'utente non cambi esplicitamente argomento o razza."
    )
}

async def detect_language(text):
    if any(ch in text for ch in "àèéìòù"):
        return "it"
    return "en"

async def process_message(msg: types.Message, vector_store):
    text = msg.text.strip()
    lang = user_lang.get(msg.from_user.id, await detect_language(text))
    user_id = str(msg.from_user.id)

    if text.lower() in ["english", "italiano"]:
        user_lang[msg.from_user.id] = LANGUAGES[text]
        await msg.answer(f"Language set to: {text}", reply_markup=kb)
        return

    if text.lower() == "clear memory":
        user_history[user_id] = []
        save_user_history(user_history)
        await msg.answer("Memory cleared.", reply_markup=kb)
        return

    if text.lower() == "resents":
        history = user_history.get(user_id, [])
        if not history:
            await msg.answer("History is empty.", reply_markup=kb)
        else:
            history_text = "\n\n".join(
                [f"*Q:* {q}\n*A:* {a}" for q, a in history[-MAX_HISTORY:]]
            )
            await msg.answer(history_text, reply_markup=kb, parse_mode=ParseMode.MARKDOWN)
        return

    logger.info(f"Query from user {msg.from_user.id} ({lang}): {text}")

    history = user_history.get(user_id, [])
    previous_q1 = history[-1][0] if len(history) > 0 else ""
    previous_q2 = history[-2][0] if len(history) > 1 else ""

    search_query = " ".join(q for q in [previous_q2, previous_q1, text] if q and q.strip().lower() not in ["resents", "clear memory", "english", "italiano"])

    results_with_score = vector_store.similarity_search_with_score(search_query, k=3)
    filtered = [doc for doc, score in results_with_score if score > 0.3]

    if not filtered:
        fallback_text = {
            "en": "Sorry, I can only answer questions related to the Weimaraner breed.",
            "it": "Mi dispiace, posso rispondere solo a domande relative alla razza Weimaraner."
        }
        await msg.answer(fallback_text[lang], reply_markup=kb)
        return

    context = "\n---\n".join([doc.page_content for doc in filtered])

    if lang == "it":
        prompt = (
            "Rispondi esclusivamente a domande relative alla razza Weimaraner, "
            "utilizzando solo i fatti contenuti nel contesto fornito. "
            "Se la domanda non è pertinente o non c'è abbastanza contesto, "
            "scrivi semplicemente che non lo sai.\n\n"
            f"Domande recenti dell'utente: {previous_q2} {previous_q1}\n"
            f"Domanda attuale: {text}\n"
            f"Contesto: {context}\n"
            "Risposta:"
        )
    else:
        prompt = (
            "Answer ONLY questions related to the Weimaraner breed, "
            "using ONLY the facts provided in the context below. "
            "If the question is off-topic or there isn't enough context, "
            "just say you don't know.\n\n"
            f"User's recent questions: {previous_q2} {previous_q1}\n"
            f"Current question: {text}\n"
            f"Context: {context}\n"
            "Answer:"
        )

    completion = await openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT[lang]},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1200
    )
    answer = completion.choices[0].message.content.strip()

    user_history.setdefault(user_id, [])
    user_history[user_id].append((text, answer))
    if len(user_history[user_id]) > MAX_HISTORY:
        user_history[user_id] = user_history[user_id][-MAX_HISTORY:]
    save_user_history(user_history)

    await msg.answer(answer, reply_markup=kb, parse_mode=ParseMode.MARKDOWN)

@dp.message(Command("start"))
async def start(msg: types.Message):
    user_lang[msg.from_user.id] = DEFAULT_LANG
    await msg.answer(
        "Hi! I am an AI FAQ bot for the Weimaraner breed. Ask your question!",
        reply_markup=kb
    )

@dp.message()
async def handle(msg: types.Message):
    await process_message(msg, vector_store)

if __name__ == "__main__":
    logger.add("bot.log", rotation="500 KB")

    if not os.path.exists("vector_db.ok"):
        text = load_faq_docs_docx("data/weimaraner_faq.docx")
        docs = split_docs(text)
        build_vector_store(docs)
        with open("vector_db.ok", "w") as f:
            f.write("built")
        logger.info("Vector store built and uploaded!")
    else:
        logger.info("Vector store already built.")

    vector_store = get_vector_store()
    logger.info("Bot started.")
    asyncio.run(dp.start_polling(bot))
