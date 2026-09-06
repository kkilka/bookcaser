from bs4 import BeautifulSoup
import urllib.request
import requests
import time
import selenium


headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Cookie': '<ВСТАВЬТЕ_СВОИ_COOKIE_LIVELIB>', 'Host': 'www.livelib.ru', 'Pragma': 'no-cache', 'Referer': 'https://www.livelib.ru/find/%D0%BA%D0%B0%D1%84%D0%B5+%D0%BD%D0%B0+%D0%BA%D1%80%D0%B0%D1%8E+%D0%B7%D0%B5%D0%BC%D0%BB%D0%B8', 'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}
quote_headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Cookie': '<ВСТАВЬТЕ_СВОИ_COOKIE_LIVELIB>', 'Host': 'www.livelib.ru', 'Pragma': 'no-cache', 'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'none', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

class Book:
    def __init__(self, title: str, url: str, cover_url: str, author: str, rating: float, quotes_page: str, review_page: str, book_id: int):
        self.title = title
        self.url = url
        self.cover_url = cover_url
        self.author = author
        self.rating = rating
        self.quotes_page = quotes_page
        self.review_page = review_page
        self.book_id = book_id


class Review:
    def __init__(self, text: str, rating: int):
        self.text = text
        self.rating = rating

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
    

def search_book(name: str = None, url: str = None) -> Book:
    session = requests.Session()

    if name and not url:
        request_url = f'https://www.livelib.ru/find/books/{name.replace(" ", "+")}'
        request = session.get(request_url, headers=headers)
        
        soup = BeautifulSoup(request.text, 'lxml')

        url = 'https://www.livelib.ru' + soup.find('div', 'brow-title').find('a')['href']

    request = session.get(url, headers=headers)
    soup = BeautifulSoup(request.text, 'lxml')

    title = soup.find('h1', 'bc__book-title').text
    cover_url = soup.find('div', 'bc-menu__image-wrapper').find('img')['src']
    author = soup.find('a', 'bc-author__link').text
    rating = soup.find('a', 'bc-rating-medium').find('span').text.replace(',', '.')
    quotes_page = 'https://www.livelib.ru' + soup.find('a', 'bc-detailing-quotes bc-header__link')['href']
    review_page = 'https://www.livelib.ru' + soup.find('a', 'bc-header__link bc-detailing-reviews')['href']
    book_id = int(cover_url.split('/')[4])

    return Book(title, url, cover_url, author, rating, quotes_page, review_page, book_id)


def get_review(book: Book):
    review_headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Content-Length': '58', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cookie': '<ВСТАВЬТЕ_СВОИ_COOKIE_LIVELIB>', 'Host': 'www.livelib.ru', 'Origin': 'https://www.livelib.ru', 'Pragma': 'no-cache', 'Referer': book.review_page, 'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'}
    session = requests.Session()

    session.get(book.url, headers=headers)
    request = session.get(book.review_page, headers=headers)
    soup = BeautifulSoup(request.text, 'lxml')

    if len(soup.find_all('a', 'pagination__page')) > 0:
        page_count = int(soup.find_all('a', 'pagination__page')[-1]['href'].split('~')[-1])
    else:
        page_count = 1

    for i in range(1, page_count+1):
        request = session.get(book.review_page+'/~'+str(i), headers=headers)
        soup = BeautifulSoup(request.text, 'lxml')

        for j in soup.find_all('div', 'review-card lenta__item'):
            review_id = j.find('a', 'sab__link icon-share').find('span')['id'].split('-')[-1]
            
            if len(j.find_all('span', 'lenta-card__mymark')) > 0: 
                rating = float(j.find('span', 'lenta-card__mymark').text)
            else:
                rating = None

            sac_data = {'object_alias': 'review', 'object_id': review_id, 'type': 'expand', 'is_new_design': ''}
            getfullobject_data = {'object_alias': 'review', 'object_id': review_id, 'is_new_design': 'll2019'}

            session.post('https://www.livelib.ru/service/sac', headers=review_headers, data=sac_data)
            r = session.post('https://www.livelib.ru/feed/getfullobjecttext', headers=review_headers, data=getfullobject_data)

            yield Review(BeautifulSoup(r.json()['content'], 'lxml').text, rating)


def get_quote(book: Book) -> list[Quote]:
    quotes = list()
    session = requests.Session()

    session.get(book.url, headers=headers)
    request = session.get(book.quotes_page, headers=headers)
    soup = BeautifulSoup(request.text, 'lxml')
    
    if len(soup.find_all('a', 'pagination__page')) > 0:
        page_count = int(soup.find_all('a', 'pagination__page')[-1]['href'].split('~')[-1])
    else:
        page_count = 1

    for i in range(1, page_count+1):
        request = session.get(book.quotes_page+'/~'+str(i), headers=headers)
        soup = BeautifulSoup(request.text, 'lxml')

        for j in soup.find_all('div', 'quote-card lenta__item'):
            quote = j.find('div', 'lenta-card').find('p').text

            if len(quote) > 100 or len(quote) < 50: continue
            
            for k in ['"', 'ⓒ', '©', '«', '»']:
                if k in quote: break
            else:
                quotes.append(Quote(quote.strip(), None))
                if len(quotes) == 3: return quotes    
        
    return quotes
        

def get_genre(book: Book) -> list[str]:
    request = requests.get(book.url, headers=headers)
    soup = BeautifulSoup(request.text, 'lxml')

    return list(map(lambda x: x['href'].split('/')[2].replace('-', ' '), soup.find('ul', 'bc-genre__list').find_all('a')))


def get_description(book: Book) -> list[str]:
    r = requests.post('https://www.livelib.ru/feed/getfullobjecttext', data={'object_alias': 'edition', 'object_id': str(book.book_id), 'is_new_design': 'll2019'}, headers={'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Content-Length': '62', 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'Cookie': '<ВСТАВЬТЕ_СВОИ_COOKIE_LIVELIB>', 'Host': 'www.livelib.ru', 'Origin': 'https://www.livelib.ru', 'Pragma': 'no-cache', 'Referer': 'https://www.livelib.ru/book/1007053420-glyadya-na-more-fransuaza-burden', 'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36', 'X-Requested-With': 'XMLHttpRequest'})
    return BeautifulSoup(r.json()['content'], 'lxml').text


def get_cover(book: Book):
    urllib.request.urlretrieve(book.cover_url, f'temp\\{book.book_id}.png')
    return f'temp\\{book.book_id}.png'

# for j in get_review(search_book('Сказать жизни «Да!»: психолог в концлагере')):
    # print(j)