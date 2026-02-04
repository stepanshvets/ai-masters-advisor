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

- Retrieval: Векторный база данных, в которую входят тексты html-страниц программ и структурированная инф-ия по учебным планам

- Generation: GPT-4o для генерации ответов

Также для каждого пользователя хранится свой контекст

### 2. Data Pipeline
Интернет-источники → Парсинг → Обработка → Векторная база

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;          ↓

HTML страницы       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;BeautifulSoup  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;spacy   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;документ (через llama-index)

PDF учебные планы  &nbsp; pdfplumber    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;ChatGPT    &nbsp;&nbsp; структурированный блок в llama-index с мета-инф.

Обработка текстовый информации для html-страниц состоит из:
1. Очистка html-страницы с помощью BeutifulSoup
2. Токенизация
3. Фильтрация "мусора" и удаление стоп-слов
4. Лемматизация
5. Нормализация - приведение к нижнему регистру

Учебные планы перегнали в json с помощью ChatGPT, чтобы структурировать информацию для векторной базы данных

Более подробно смотрите в notebook

### 3. Telegram Bot 
Обработка сообщений пользователей, для каждого пользователя хранится свой контекст

![photo_2026-02-04_18-36-45](https://github.com/user-attachments/assets/d6a85bea-6236-4262-8740-34e792b9879d)

![photo_2026-02-04_18-37-03](https://github.com/user-attachments/assets/ea3bda28-38cc-4dfc-b5fc-ab9041baa29b)

