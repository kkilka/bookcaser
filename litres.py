from bs4 import BeautifulSoup
import urllib.request
import requests


class Book:
    def __init__(self, title: str, url: str, cover_url: str, author: str, author_rodit: str, rating: float, id: int, full_data: dict):
        self.title = title
        self.url = url
        self.cover_url = cover_url
        self.author = author
        self.author_rodit = author_rodit
        self.rating = rating
        self.id = id
        self.full_data = full_data


class Review:
    def __init__(self, review_data: dict, book: Book):
        self.text: str = review_data['text'][3:-4]
        self.rating: int = review_data['item_rating']
        self.id: int = review_data['id']
        self.book = book

    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return self.text
    

class Quote:
    def __init__(self, text: str, rating: int):
        self.text = text
        self.rating = rating

    def __str__(self) -> str:
        return self.text
    
    def __repr__(self) -> str:
        return self.text


def search_book(name: str) -> Book:
    request_url = f'https://api.litres.ru/foundation/api/search?limit=12&q={name.replace(" ", "+")}&types=text_book'

    request = requests.get(request_url)

    open('book.json', 'w', encoding='utf-8').write(request.text)

    book_data = request.json()['payload']['data'][0]['instance']
    title = book_data['title']
    url = 'https://litres.ru' + book_data['url']
    cover_url = 'https://litres.ru' + book_data['cover_url']
    author = book_data['persons'][0]['full_name']
    author_rodit = book_data['persons'][0]['full_rodit']
    rating = round(book_data['rating']['rated_avg'], 1)
    id = book_data['id']

    return Book(title, url, cover_url, author, author_rodit, rating, id, book_data)


def get_review_old(book: Book, request_url: str = None, reviews: dict = {1: list(), 2: list(), 3: list(), 4: list(), 5: list()}) -> dict:
    for i in reviews.values():
        if len(i) == 3: continue
        break
    else:
        return reviews

    if request_url == None:
        request_url = f'https://api.litres.ru/foundation//api/arts/{book.id}/reviews?limit=1&o=popular'

    request = requests.get(request_url)
    review = Review(request.json()['payload']['data'][0], book)

    if review.text.count(' ') <= 50 and review.rating != None and len(reviews[review.rating]) < 3:
        reviews[review.rating].append(review)

    if request.json()['payload']['pagination']['next_page'] != None:
        next_review_url = 'https://api.litres.ru/foundation/' + request.json()['payload']['pagination']['next_page']
        return get_review_old(book, next_review_url, reviews)
    else:
        return reviews


def get_review(book: Book):
    request_url = f'https://api.litres.ru/foundation//api/arts/{book.id}/reviews?limit=50&o=popular'
    request = requests.get(request_url)
    request_data = request.json()['payload']

    while request_data['pagination']['next_page'] != None:
        request = requests.get(request_url)
        request_data = request.json()['payload']

        for i in request_data['data']:
            yield Review(i, book)
        
        if request_data['pagination']['next_page'] != None:
            request_url = 'https://api.litres.ru/foundation/' + request_data['pagination']['next_page']


def get_quote(book: Book) -> list:
    quotes = list()

    request_url = book.url + 'citaty'
    request = requests.get(request_url)

    soup = BeautifulSoup(request.text, 'lxml')
    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('div', class_='quote__text').text
        rating = int(quote.find('span', class_='quote__rating').text)

        if len(text) < 400:
            quotes.append(Quote(text, rating))

    return quotes[:3]


def get_description(book: Book) -> str:
    request = requests.get(book.url)
    soup = BeautifulSoup(request.text, 'lxml')

    return soup.find_all('div', class_='BookCard_book__annotation__8wq0r')[-1].text


def get_genre(book: Book) -> list:
    genres = list()

    request = requests.get(book.url)
    soup = BeautifulSoup(request.text, 'lxml')

    for element in soup.find_all('a', class_='BookGenresAndTags_genresList__item__cNfnw'):
        if 'genre' in element['href']:
            genres.append(element.text)

    return genres[:3]


def get_cover(book: Book):
    urllib.request.urlretrieve(book.cover_url, f'temp\\{book.id}.png')
    return f'temp\\{book.id}.png'