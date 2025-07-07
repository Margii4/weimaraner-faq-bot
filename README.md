 🐶 AI FAQ Telegram Bot for the Weimaraner Breed

A multilingual, context-aware FAQ Telegram bot powered by Retrieval Augmented Generation (RAG), OpenAI LLM, and semantic search.  
Built to answer user questions about the Weimaraner dog breed with reliable, factual information from your custom FAQ knowledge base.

---

   ✨ Features

- 🧠 Retrieval Augmented Generation (RAG): Finds and uses the most relevant context from your FAQ document for each user question.
- 🌐 Multilingual Support: Understands and answers in both English and Italian. Language is auto-detected and can be switched on-the-fly.
- 🪄 Prompt Engineering: Uses dynamic system prompts for native, professional answers, adapting style to language and audience.
- 🔎 Semantic Search: Pinecone + OpenAI Embeddings for accurate, meaning-based retrieval of information, not just keyword matches.
- 🤖 Rich User Experience:
  - 💬 Interactive Telegram interface with quick language switching.
  - 🕑 Recent conversation history ("Resents" button) shows last 5 Q/A for each user.
  - 🧹 "Clear memory" button to reset user history.
- 💾 Persistent User Data: Remembers user language and question history between sessions (local JSON storage).
- 🛡️ Context-Safe: Will not hallucinate or make up facts not found in the FAQ.
- ⚡ Modern Async Python: Fast, responsive, scalable with aiogram 3 and asyncio.

---

   🛠️ Technologies Used

-🐍 Python 3.10+ — Core programming language.
- 🤖 aiogram 3 — Modern async Telegram bot framework.
- 🧩 OpenAI GPT (gpt-3.5-turbo) — Language model for generating answers.
- 🧬 OpenAI Embeddings — For turning text into semantic vectors.
- 🗄️ Pinecone — Managed vector database for high-performance semantic search.
- 🔗 LangChain — RAG orchestration and document splitting.
- 📄 docx2txt — Loads and processes `.docx` FAQ documents.
- 🗝️ dotenv — Manages configuration via `.env` files.
- 📋 loguru — Simple, powerful logging.
- 📝 JSON — Persistent storage of user history.
- 📦 requirements.txt — Easy dependency management.


# 🚀 Getting Started

1. **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/weimaraner-faq-bot.git
    cd weimaraner-faq-bot
    ```
    _Clones the repository and enters the project folder._

2. **Create and activate a virtual environment**
    ```bash
    python -m venv venv
    ```
    - **For Windows:**
      ```bash
      venv\Scripts\activate
      ```
    - **For Linux/macOS:**
      ```bash
      source venv/bin/activate
      ```
    _Creates and activates an isolated Python environment._

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    _Installs all required dependencies from requirements.txt._

4. **Set up environment variables**
    - Create a `.env` file in the project root with the following content:
      ```env
      TELEGRAM_BOT_TOKEN=your-telegram-token          # Your Telegram bot token
      OPENAI_API_KEY=your-openai-key                  # Your OpenAI API key
      PINECONE_API_KEY=your-pinecone-key              # Your Pinecone API key
      PINECONE_INDEX=your-index-name                  # Your Pinecone index name
      ```
    _This sets all necessary environment variables._

5. **Add your FAQ document**
    - Place your (English) FAQ as:
      ```
      data/weimaraner_faq.docx
      ```
    _This document will be processed and indexed._

6. **Run the bot**
    ```bash
    python bot.py
    ```
    - On the first run, the FAQ will be split, indexed, and uploaded to Pinecone.
    - The bot will start polling for messages in Telegram.

---

### 📝 Usage

- Open Telegram and find your bot.
- Use the `/start` command to begin.
- Ask questions in English or Italian about Weimaraners.
- Use keyboard buttons to switch language, view recent questions ("Resents"), or clear chat history ("Clear memory").

On first run, the FAQ will be split, indexed, and uploaded to Pinecone.

Bot will start polling for messages in Telegram.

---

📱 Usage

📲 Open Telegram and find your bot.

🚀 Use /start to begin.

❓ Ask questions in English or Italian about Weimaraners.

🗂️ Use keyboard buttons to switch language, show your recent question history, or clear your memory.

📝 Example questions:

"What are the main characteristics of the Weimaraner breed?"

"Quali sono i problemi di salute comuni nei Weimaraner?"

---

⚡ Example Prompt Engineering (EN/IT)
English system prompt:
“You are a native English canine expert. Answer ONLY in natural, correct, literary English. Never translate phrases literally from other languages. If you don't know the answer from context, just say you don't know.”

Italian system prompt:
“Sei un esperto cinofilo madrelingua italiano. Rispondi SOLO in italiano naturale, corretto e professionale, evitando calchi o traduzioni letterali da altre lingue. Se non sai la risposta dal contesto, scrivi semplicemente che non lo sai.”

---

## License

MIT

   



🚀 Author
Margarita Viviers


