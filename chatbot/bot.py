import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.llms.openai import OpenAI
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core import Settings
from llama_index.core.workflow import Context

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Токены не заданы в ENV")

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()

async def search_documents(query: str) -> str:
    response = await query_engine.aquery(query)
    return str(response)

Settings.llm = OpenAI(
    model="gpt-4o",
    temperature=0.1,
    max_tokens=1000
)

agent = FunctionAgent(
    tools=[search_documents],
    llm=Settings.llm,
    system_prompt="""Ты консультант по магистерским программам в области ИИ.

РОЛЬ:
Помогаешь абитуриентам выбрать между программами:
1. "Искусственный интеллект" - техническая, для разработчиков и исследователей
2. "Управление ИИ-продуктами/AI Product" - управленческая, для продуктовых менеджеров

ИСТОЧНИКИ ИНФОРМАЦИИ:
У тебя есть доступ к учебным планам и описаниям программ.

ИНСТРУКЦИИ:
1. Сначала спроси о бэкграунде абитуриента (технический/нетехнический, опыт, интересы)
2. Основывай ответы на информации из базы данных
3. Давай конкретные рекомендации по выбору курсов
4. Объясняй различия программ простым языком
5. Не упоминай детали (зачётные единицы, часы) без запроса
6. Формат ответов: простой текст, без markdown, для Telegram

СТРУКТУРА ДИАЛОГА:
1. Узнай цели абитуриента
2. Сравни программы по ключевым критериям
3. Предложи 2-3 подходящих курса для первого семестра
4. Дай итоговую рекомендацию

ПРИМЕРЫ ХОРОШИХ ОТВЕТОВ:
"Если у вас технический бэкграунд и хотите разрабатывать модели ИИ - выбирайте 'Искусственный интеллект'. Для первого семестра рекомендую 'Машинное обучение' и 'Обработку данных'."

"Для менеджеров продуктов подходит 'Управление ИИ-продуктами'. Начните с 'Продуктовых исследований' и 'Монетизации ИИ-продуктов'."

Задавай уточняющие вопросы, если информации недостаточно, но только по необходимости! На вопрос: Подскажи, в чем основные различия между учебными планами двух программ - ты сможешь ответить сам.""",
)

context_manager = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    username = user.username
    
    print(f"🚀 START | ID: {user_id} | @{username}")
    
    welcome_text = (
        f"👤 ID: {user_id}\n\n"
        "Здравствуйте! Я ИИ-ассистент, который поможет Вам в выборе магистерских программ - "
        "Искусственный интеллект и Управление ИИ-продуктами. "
        "Также я могу помочь с выбором дисциплин, которые реализуются в данных программах.\n\n"
        "Задавайте вопросы!"
    )
    
    await update.message.reply_text(welcome_text)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    user_id = user.id
    username = user.username
    
    print(f"MESSAGE | ID: {user_id} | @{username} | Text: {update.message.text}")
    
    text = update.message.text
    
    try:
        context = None
        if user_id in context_manager:
            context = context_manager[user_id]
        else:
            context = Context(agent)
            context_manager[user_id] = context
        response = await agent.run(text, ctx=context)
        ai_response = str(response)
    except Exception as e:
        print(f"❌ Error: {e}")
        ai_response = "Извините, произошла ошибка при обработке запроса."
    
    final_response = f"👤 ID: {user_id}\n@{username}\n\n{ai_response}"
    
    await update.message.reply_text(final_response)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Бот готов!")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
