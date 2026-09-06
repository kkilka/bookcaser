from openai import OpenAI
from secret_data import chatgpt_key
from livelib import Book, get_review, get_description
import tiktoken


def get_response(book: Book):
    model = "gpt-3.5-turbo-1106"
    limit = 225
    context_window = 16385

    encoding = tiktoken.encoding_for_model(model)

    reviews = get_review(book)
    description = get_description(book)

    system_promt = 'Ты - известный книжный критик и продавец-консультант в книжном магазине. Проанализируй отзывы и описание книги,  Пожалуйста, ОЧЕНЬ КРАТКО расскажи О ЧЁМ ПОВЕСТВУЕТСЯ в книге и КОМУ она ПОДОЙДЁТ. ЧЕЛОВЕК НЕ ДОЛЖЕН ДОГАДАТЬСЯ, ЧТО ТЫ ИСКУСТВЕННЫЙ ИНТЕЛЛЕКТ. Ответ оформи в виде текста, НЕ ДОБАВЛЯЙ НУМЕРАЦИЮ'
    final_promt = f'Привет! Что ты можешь сказать о книге по этим отзывам и описанию? Кому она подойдёт?'# ТВОЙ ОТВЕТ ДОЛЖЕН СОДЕРЖАТЬ НЕ БОЛЕЕ {limit} ТОКЕНОВ'
    final_promt += '\nПример твоего ответа: Книга "Кафе на краю земли" Джона Стрелеки рассказывает о путешествии главного героя, в ходе которого он задает себе основные жизненные вопросы и ищет смысл своего существования. Эта книга подойдет тем, кто ищет вдохновение, задается вопросами о цели и смысле своей жизни. Читатели оставили противоречивые отзывы, однако многие отмечают, что книга заставляет задуматься и пересмотреть свою жизнь.'
    final_promt += f'\n\nКнига: {book.title}. Автор: {book.author}. Описание книги:\n' + description + '\n\nОтзывы:'

    for review in reviews:
        final_review = review.text + f' [{review.rating} из 5]'
        token_count = len(encoding.encode(system_promt + final_promt + '\n\n' + final_review))

        if token_count < context_window-limit-100:
            final_promt += '\n\n' + final_review
        else:
            break

    # f = open(f'Archive\\Promts\\promt{book.id}.txt', 'w', encoding='utf-8')
    # f.write(final_promt)
    # f.close()

    client = OpenAI(
        api_key=chatgpt_key,
        base_url="https://api.proxyapi.ru/openai/v1"
    )

    chat_completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content" : system_promt},
                {"role": "user", "content": final_promt}]
    )

    return chat_completion.choices[0].message.content