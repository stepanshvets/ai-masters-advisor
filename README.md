Будет очень здорово, если сообщите, что удалось проверить работу: issues или сообщение в тг. В любом случае, спасибо, что здесь! :)

# AI Masters Advisor

ИИ-ассистент, который поможет абитуриенту выбрать одну из двух магистерских программ - 
Искусственный интеллект и и Управление ИИ-продуктами. 
Ассистент поможет ответить на все необходимые вопросы по программам, спланировать учебу и определиться с выбором дисциплин.

## Использование

Использовать ассистент можно уже прямо сейчас https://t.me/ai_masters_advisor_bot

По всем вопросам и в случае неполадок обращайтесь к https://t.me/stepanshvets

Также все можно развернуть самостоятельно:

```
cd ./chatbot
docker build -t ai-masters-bot .
docker run -d --name ai-bot ai-masters-bot
```

## Реализация

### 1. RAG (Retrieval-Augmented Generation) Engine

Основан на библиотеке llama-index. Состоит из двух частей:

- Retrieval: Векторный поиск по документам

- Generation: GPT-4o-mini для генерации ответов

Также для каждого пользователя хранится свой контекст

### 2. Data Pipeline
Интернет-источники → Парсинг → Обработка → Векторная база

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;          ↓

HTML страницы       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;BeautifulSoup  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;spacy   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(через llama-index)

PDF учебные планы  &nbsp; pdfplumber    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;spacy    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(через llama-index)

Обработка состоит из:
1. Токенизация
2. Фильтрация "мусора" и удаление стоп-слов
3. Лемматизация
4. Нормализация - приведение к нижнему регистру

### 3. Telegram Bot 
Обработка сообщений пользователей

