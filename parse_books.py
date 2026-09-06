import requests
from bs4 import BeautifulSoup
import csv

f = open('books.txt', 'w', encoding='utf-8')

for i in range(1, 5000):
    link = f'https://www.litres.ru/collections/knigi-ot-livelib/?art_types=text_book&page={i}'
    
    request = requests.get(link)
    soup = BeautifulSoup(request.text, 'lxml')

    for j in soup.find_all('div', 'ArtsGrid_artWrapper__LXa0O'):
        try:
            title = j.find('p', 'ArtInfo_title__h_5Ay').text
            author = j.find('a', 'ArtInfo_author__0W3GJ').text
        except:
            pass

        line = f'{author} : {title}'
        if line == 'Эдит Ева Эгер : Выбор. О свободе и внутренней силе человека' and i != 1: exit(0)
        
        f.write(line + '\n')
        print(line)
