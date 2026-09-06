# import urllib.request
# import requests
# import json


# def voice_over(text: str) -> str:
#     session = requests.Session()

#     headers = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Pragma': 'no-cache', 'Referer': 'https://texttospeech.ru/', 'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'Token': '<ВСТАВЬТЕ_СВОЙ_TOKEN>', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

#     payload = json.dumps({"rate": "0", "pitch": "0", "volume": "0", 'bitrate': "320kb/s", "shift": "0", "echo": "0", "text": text, "code": "ru-RU094", "format": "mp3"})
#     headers2 = {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate, br, zstd', 'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7', 'Cache-Control': 'no-cache', 'Content-Type': 'text/plain;charset=UTF-8', 'Origin': 'https://texttospeech.ru', 'Pragma': 'no-cache', 'Referer': 'https://texttospeech.ru/', 'Sec-Ch-Ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"', 'Sec-Ch-Ua-Mobile': '?0', 'Sec-Ch-Ua-Platform': '"Windows"', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin', 'Token': '<ВСТАВЬТЕ_СВОЙ_TOKEN>', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

#     session.get('https://texttospeech.ru/api/v1/user', headers=headers)
#     r = session.post('https://texttospeech.ru/api/v1/synthesize', headers=headers2, data=payload)

#     audio_link = 'https://texttospeech.ru/' + str(r.json()['data']['filelink'])
#     path = 'temp\\' + audio_link.split('/')[-1]

#     urllib.request.urlretrieve(audio_link, path)
#     return path


from openai import OpenAI
from secret_data import chatgpt_key
import time


client = OpenAI(api_key=chatgpt_key,
        base_url="https://api.proxyapi.ru/openai/v1")


def voice_over(text: str):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text)

    path = f'temp\\speech_{time.time()}.mp3'
    response.write_to_file(path)
    return path

# print(len('Время для очередного книжного путешествия! Готовы отправиться?'))

# voice_over('А вы читали эту книгу??? Напишите своё мнение о ней в комментариях.')