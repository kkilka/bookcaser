from data import command, hashtags
from livelib import search_book
from datetime import datetime, timezone, timedelta
import os
import pandas

from telegram_bot import send_post
from chat_gpt import get_response
from makevideo import make_video

import pickle 


def publish(time: datetime):
    uploaded_books_table = pandas.read_csv('uploaded_books.csv')
    books_table = pandas.read_csv('books_data.csv')
    error_table = pandas.read_csv('error_books.csv')

    book_row = books_table[(~books_table['Ссылка на произведение'].isin(uploaded_books_table['Ссылка на произведение'])) & \
                        (~books_table['Ссылка на произведение'].isin(error_table['Ссылка на произведение']))].sample(n=1)

    for _ in range(5):
        try:
            book = search_book(book_row['Ссылка на произведение'].item())
            book.title = book_row['Произведение'].item()
            book.author = book_row['Автор'].item()
            
            response = get_response(book)
            make_video(book, response)

            send_post(book, response, time)
            os.system(command.format(book.title.replace('"', '\\"'), book.author, response.replace('"', '\\"'), hashtags, time.isoformat()))

            book_row.to_csv('uploaded_books.csv', mode='a', index=False, header=None)
            return
        except Exception as exp:
            last_exp = exp
            print(f'Attempt to get the book was unsuccesful! [{exp}]')
    else:
        book_row['Ошибка'] = last_exp
        book_row.to_csv('error_books.csv', mode='a', index=False, header=None)
        publish(time)


# time = datetime(year=2024, month=6, day=29, hour=16, minute=0, tzinfo=timezone(timedelta(hours=7)))
# pickle.dump(time, open('last.publishtime', 'wb'))
# exit(0)

# publish(time)

for _ in range(6): 
    time = pickle.load(open('last.publishtime', 'rb')) 
    time += timedelta(1) 
 
    print('publish to', time)
    publish(time)
    pickle.dump(time, open('last.publishtime', 'wb'))


# print(f'python youtube_api.py --file="temp/output.mp4" --title="Джордж Мартин. \\"Игра престолов\\"" --description="Книга \\"Игра престолов\\" Джорджа Мартина рассказывает о битвах за власть и трон, политических интригах, а также о приключениях различных персонажей в интересном фэнтезийном мире. Эта книга подойдет тем, кто ценит многообразие персонажей, сложные сюжетные повороты и погружение в детали миростроения. В то же время, она также подойдет для любителей политических интриг и фэнтезийных приключений." --keywords="{hashtags}" --category="27" --privacyStatus="private" --time="{time.isoformat()}"')