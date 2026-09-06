import telebot
from secret_data import tgbot_token, api_id, api_hash
from livelib import get_quote, get_genre, Book
from preview import get_preview
from chat_gpt import get_response

from livelib import search_book

from telethon import TelegramClient
from datetime import datetime, timedelta, timezone

# 📚💫💭🗯💬💥🍀☘🌿🔥✨


def send_post(book: Book, response: str, shedule: datetime):
    preview = open(get_preview(book), 'rb')
    response = '🔥 ' + response

    jernes = ', '.join(get_genre(book))

    post = f'📚 <b>{book.author}. "{book.title}"</b>\n\n✨ <b>Жанр:</b> {jernes}\n\n{response}'

    quotes = get_quote(book)
    quotes_text = str()
    title = f'\n\n🍀 <b>Цитаты из книги:</b>\n'
    for quote in quotes:
        if quote.text[-1] == '.': quote.text = quote.text[:-1]
        quote.text = '«' + quote.text + '» ©'

        # if quote.text[-1] not in ['.', '!', '?']: quote.text += '.'

        quote = f'<blockquote>💭 <i>{quote}</i></blockquote>\n'
        if len(post) + len(quotes_text) + len(quote) + len(title) > 1024:
            break
        quotes_text += quote

    if len(quotes_text) > 0:
        post += title + quotes_text

    client = TelegramClient('anon', api_id, api_hash, system_version="4.16.30-vxCUSTOM")
    with client:
        client.loop.run_until_complete(client.send_message('https://t.me/+N1-2EdlPgewwYWYy', post, parse_mode='html', file=preview, force_document=False, schedule=shedule))#=datetime(year=2024, month=5, day=2, hour=18, minute=55, tzinfo=timezone(timedelta(hours=7)))))

# send_post(search_book('Звезда пленительного счастья'), 'Книга "Гордость и предубеждение" Джейн Остин рассказывает о жизни английской аристократии XIX века и истории любви главной героини, Элизабет Беннет, и мистера Дарси. Эта книга подойдет тем, кто любит классические романтические произведения, ценит тонкое чувство юмора и интересуется английским обществом XVIII века. В книге множество живописных персонажей, увлекательные диалоги и неповторимая атмосфера эпохи, которая заставляет задуматься о принципах и ценностях жизни.', datetime(year=2024, month=6, day=15, hour=16, minute=0, tzinfo=timezone(timedelta(hours=7))))