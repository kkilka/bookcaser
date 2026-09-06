import requests
from bs4 import BeautifulSoup
from time import sleep


headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Cookie': '<ВСТАВЬТЕ_СВОИ_COOKIE_LIVELIB>', 'Host': 'www.livelib.ru', 'Pragma': 'no-cache', 'Referer': 'https://www.livelib.ru/find/%D0%BA%D0%B0%D1%84%D0%B5+%D0%BD%D0%B0+%D0%BA%D1%80%D0%B0%D1%8E+%D0%B7%D0%B5%D0%BC%D0%BB%D0%B8', 'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Site': 'same-origin', 'Sec-Fetch-User': '?1', 'Upgrade-Insecure-Requests': '1', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

# links_body = ['https://www.livelib.ru/genre/%D0%9A%D0%BB%D0%B0%D1%81%D1%81%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B0%D1%8F-%D0%BB%D0%B8%D1%82%D0%B5%D1%80%D0%B0%D1%82%D1%83%D1%80%D0%B0', 'https://www.livelib.ru/genre/%D0%97%D0%B0%D1%80%D1%83%D0%B1%D0%B5%D0%B6%D0%BD%D0%B0%D1%8F-%D0%BB%D0%B8%D1%82%D0%B5%D1%80%D0%B0%D1%82%D1%83%D1%80%D0%B0', 'https://www.livelib.ru/genre/%D0%A0%D1%83%D1%81%D1%81%D0%BA%D0%B0%D1%8F-%D0%BB%D0%B8%D1%82%D0%B5%D1%80%D0%B0%D1%82%D1%83%D1%80%D0%B0', 'https://www.livelib.ru/genre/%D0%94%D0%B5%D1%82%D0%B5%D0%BA%D1%82%D0%B8%D0%B2%D1%8B', 'https://www.livelib.ru/genre/%D0%A4%D1%8D%D0%BD%D1%82%D0%B5%D0%B7%D0%B8', 'https://www.livelib.ru/genre/%D0%A4%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0', 'https://www.livelib.ru/genre/%D0%A1%D0%BE%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F-%D0%BF%D1%80%D0%BE%D0%B7%D0%B0', 'https://www.livelib.ru/genre/%D0%9F%D1%80%D0%B8%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D1%8F', 'https://www.livelib.ru/genre/%D0%A3%D0%B6%D0%B0%D1%81%D1%8B-%D0%BC%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B0', 'https://www.livelib.ru/genre/%D0%9B%D1%8E%D0%B1%D0%BE%D0%B2%D0%BD%D1%8B%D0%B5-%D1%80%D0%BE%D0%BC%D0%B0%D0%BD%D1%8B', 'https://www.livelib.ru/genre/%D0%91%D0%BE%D0%B5%D0%B2%D0%B8%D0%BA%D0%B8-%D0%BE%D1%81%D1%82%D1%80%D0%BE%D1%81%D1%8E%D0%B6%D0%B5%D1%82%D0%BD%D0%B0%D1%8F-%D0%BB%D0%B8%D1%82%D0%B5%D1%80%D0%B0%D1%82%D1%83%D1%80%D0%B0', 'https://www.livelib.ru/genre/%D0%9F%D0%BE%D0%B2%D0%B5%D1%81%D1%82%D0%B8-%D1%80%D0%B0%D1%81%D1%81%D0%BA%D0%B0%D0%B7%D1%8B', 'https://www.livelib.ru/genre/%D0%9F%D0%BE%D1%8D%D0%B7%D0%B8%D1%8F-%D0%B8-%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%D1%82%D1%83%D1%80%D0%B3%D0%B8%D1%8F']
links_body = ['https://www.livelib.ru/genre/%D0%A4%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0', 'https://www.livelib.ru/genre/%D0%A1%D0%BE%D0%B2%D1%80%D0%B5%D0%BC%D0%B5%D0%BD%D0%BD%D0%B0%D1%8F-%D0%BF%D1%80%D0%BE%D0%B7%D0%B0', 'https://www.livelib.ru/genre/%D0%9F%D1%80%D0%B8%D0%BA%D0%BB%D1%8E%D1%87%D0%B5%D0%BD%D0%B8%D1%8F', 'https://www.livelib.ru/genre/%D0%A3%D0%B6%D0%B0%D1%81%D1%8B-%D0%BC%D0%B8%D1%81%D1%82%D0%B8%D0%BA%D0%B0', 'https://www.livelib.ru/genre/%D0%9B%D1%8E%D0%B1%D0%BE%D0%B2%D0%BD%D1%8B%D0%B5-%D1%80%D0%BE%D0%BC%D0%B0%D0%BD%D1%8B', 'https://www.livelib.ru/genre/%D0%91%D0%BE%D0%B5%D0%B2%D0%B8%D0%BA%D0%B8-%D0%BE%D1%81%D1%82%D1%80%D0%BE%D1%81%D1%8E%D0%B6%D0%B5%D1%82%D0%BD%D0%B0%D1%8F-%D0%BB%D0%B8%D1%82%D0%B5%D1%80%D0%B0%D1%82%D1%83%D1%80%D0%B0', 'https://www.livelib.ru/genre/%D0%9F%D0%BE%D0%B2%D0%B5%D1%81%D1%82%D0%B8-%D1%80%D0%B0%D1%81%D1%81%D0%BA%D0%B0%D0%B7%D1%8B', 'https://www.livelib.ru/genre/%D0%9F%D0%BE%D1%8D%D0%B7%D0%B8%D1%8F-%D0%B8-%D0%B4%D1%80%D0%B0%D0%BC%D0%B0%D1%82%D1%83%D1%80%D0%B3%D0%B8%D1%8F']

f = open('books.csv', 'w', encoding='utf-8')

links = list()

k = 0

for link_body in links_body:
    print('---> Genre Changed!')
    for i in range(1, 100000):
        link = link_body + f'/best/listview/biglist/~{i}'
        
        r = requests.post(link, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
            
        if soup.find('h1', 'title-404'): break

        for book_element in soup.find_all('li', class_='book-item__item book-item--full'):
            if not book_element.find('a', 'icon-review-grey') or not book_element.find('a', 'icon-quote-grey'): continue

            reviews = int(book_element.find('a', 'icon-review-grey').text.replace('K', '000'))
            quotes = int(book_element.find('a', 'icon-quote-grey').text.replace('K', '000'))

            if reviews < 300 or quotes < 300: continue

            if not book_element.find('a', class_='book-item__title')\
                  or not book_element.find('a', class_='book-item__title')\
                    or not book_element.find('a', class_='book-item__author'): continue

            url = book_element.find('a', class_='book-item__title')['href']
            title = book_element.find('a', class_='book-item__title').text
            author = book_element.find('a', class_='book-item__author').text

            if url in links or '(сборник)' in title: continue
            
            print(k, author + '.', title)
            links.append(url)
            f.write(f'"{author}","{title}","{url}"\n')

            k += 1

        sleep(1)
            