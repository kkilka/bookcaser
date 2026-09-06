from PIL import Image, ImageSequence
from mutagen.mp3 import MP3
from moviepy.editor import *
from livelib import search_book, Book, get_cover
from voiceover import voice_over
from pydub import AudioSegment 
from os import system
from PIL import Image, ImageDraw
import random

SHAPE = (1080, 1920)
# f = VideoFileClip('Source\\Masks\\mask2.mp4').resize(height=1080)
# f.write_videofile('Source\\Masks\\mask2.mp4')
# exit(0)

def make_video(book: Book, response: str):
    def _corner(bevel: int):
        image = Image.new('RGB', (bevel, bevel), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, bevel*2, bevel*2), (255, 255, 255))

        return image
    

    def frame(size: tuple, bevel: int, path: str = 'temp\\bevel.png') -> str:
        if bevel > size[0]/2 or bevel > size[1]/2: raise 'The bevel is too large for this image'

        image = Image.new('RGB', size, (255, 255, 255))
        corner = _corner(bevel)
        
        for xy in ((0, 0), (0, size[1]-bevel), (size[0]-bevel, size[1]-bevel), (size[0]-bevel, 0)):
            image.paste(corner, xy)
            corner = corner.rotate(90)

        image.save(path)
        return path

    def fade_effect(clip: VideoClip) -> VideoClip:
        mask = clip.mask.fadein(0.1).fadeout(0.1)
        clip = clip.set_mask(mask)

        return clip


    def hello_clip(duration: int|float) -> VideoClip:
        hello_clip = VideoFileClip('Source\\FinalVideos\\hello.gif', has_mask=True).set_position(('center', 'center')).speedx(1.5).set_duration(duration)

        return fade_effect(hello_clip)
    
    
    def think_clip(duration: int|float) -> VideoClip:
        hello_clip = VideoFileClip('Source\\FinalVideos\\think.gif', has_mask=True).resize(height=750).set_position(('center', 'center')).speedx(1.5).set_duration(duration)

        return fade_effect(hello_clip)


    def cover_clip(cover_path: str, duration: int|float) -> VideoClip:
        cover = ImageClip(cover_path, duration=duration).set_position(('center', SHAPE[1]//2-700)).resize(height=1000)

        mask = VideoFileClip('Source\\Masks\\mask.mp4').crop(x1=0, y1=0, x2=cover.size[0], y2=cover.size[1])
        mask2 = VideoFileClip('Source\\Masks\\mask2.mp4').crop(x1=0, y1=0, x2=cover.size[0], y2=cover.size[1]).speedx(2)
        mask2_start = cover.duration - mask2.duration

        bevel_mask = ImageClip(frame(cover.size, 25*2), duration=duration)
        bevel_mask = bevel_mask.set_mask(bevel_mask.fx(vfx.invert_colors).to_mask())

        mask = mask.set_duration(mask2_start)
        mask2 = mask2.set_start(mask2_start)

        res_mask = CompositeVideoClip(clips=[mask, mask2, bevel_mask]).to_mask()
        return cover.set_mask(res_mask)


    def demo_clip(duration: int|float):
        demo = VideoFileClip('Source\\FinalVideos\\tg_channel.mp4').set_position(('center', SHAPE[1]//2-750)).speedx(0.5).set_duration(duration)
        bevel_mask = ImageClip(frame(demo.size, 25*2), duration=demo.duration).to_mask()

        return fade_effect(demo.set_mask(bevel_mask))


    def text_clip(text: str, duration: int|float) -> VideoClip:
        text_clip = TextClip(text.replace('.', ''), fontsize=60, color='White', method='caption', size=(850, None), font='Source\\Fonts\\Involve-Bold.otf')
        text_clip = text_clip.set_position(('center', (SHAPE[1]-text_clip.size[1])//2-200)).set_duration(duration)

        return fade_effect(text_clip)


    def lowerthird_clip(duration: int|float) -> VideoClip:
        start_clip: VideoClip = VideoFileClip('Source\\FinalVideos\\a_telegram.gif', has_mask=True).resize(height=625)
        end_clip = VideoFileClip('Source\\FinalVideos\\a_telegram_reversed.gif', has_mask=True).resize(height=625)
        
        start_clip = start_clip.set_duration(duration-start_clip.duration)
        end_clip = end_clip.set_start(duration-end_clip.duration)

        # CompositeVideoClip(clips=[start_clip, end_clip]).set_position(('center', SHAPE[1]//2+200)).write_videofile(f'temp\\pidor.mp4')
        return CompositeVideoClip(clips=[start_clip, end_clip]).set_position(('center', SHAPE[1]//2+200))

    a, v = list(), list()

    def composite_video():
        cur_time = 0
        for i in range(len(video_sequence)):
            video_sequence[i] = video_sequence[i].set_start(cur_time)

            cur_time += video_sequence[i].duration + pause
        cur_time -= pause

        background = VideoFileClip('Source\\FinalVideos\\background.mp4').fx(vfx.colorx, 0.85)
        lowerthird = lowerthird_clip(cur_time-video_sequence[0].duration-pause).set_start(video_sequence[0].duration+pause)

        combined_video = CompositeVideoClip([background, lowerthird] + video_sequence)
        
        combined_video.set_duration(cur_time).write_videofile(f'temp\\video.mp4')


    def composite_audio():
        result_audio = AudioSegment.empty()
        for path in audio_sequence:
            delay = AudioSegment.silent(duration=pause//1000, frame_rate=24000)
            audio = AudioSegment.from_mp3(path).set_frame_rate(24000)

            result_audio += audio + delay

        result_audio.export('temp\\audio.mp3', bitrate='320k')


    response = response.replace('!', '!.').replace('?', '?.').split('. ')

    video_sequence = []
    audio_sequence = []
    pause = 0.15

    phrases = ['Любите книги? Мы тоже!', 'Вы в поисках новой книги? У нас есть кое-что интересное для вас.', 'Хотите найти книгу, которая вас покорит? У нас есть предложения!', 'Ищете книгу, которая вас зацепит с первой страницы? У нас есть советы!', 'Что почитать в этом месяце? Давайте узнаем вместе!', 'Вы в поисках идеальной книги для тихого вечера? Мы поможем!', 'Что почитать, чтобы забыться? Наши лучшие рекомендации!', 'Хотите открыть для себя новую любимую книгу? Смотрите это видео!', 'Ищете что-то особенное для чтения? У нас есть, что предложить!']

    # audio = voice_over(random.choice(phrases))
    audio = voice_over('Здравствуйте!')
    audio_sequence.append(audio)
    video_sequence.append(hello_clip(AudioSegment.from_mp3(audio).duration_seconds))
    
    audio = voice_over(f'Вы на канале "Книжный Шкаф" и сегодня на обзоре у нас книга "{book.title}". {book.author}')
    audio_sequence.append(audio)
    video_sequence.append(cover_clip(get_cover(book), AudioSegment.from_mp3(audio).duration_seconds))
    
    for phrase in response:
        audio = voice_over(phrase)
        audio_sequence.append(audio)
        video_sequence.append(text_clip(phrase, AudioSegment.from_mp3(audio).duration_seconds))

    audio = voice_over('А вы читали эту книгу??? Напишите своё мнение о ней в комментариях.')
    # audio = 'temp\\speech_1718296226.063948.mp3'
    audio_sequence.append(audio)
    video_sequence.append(think_clip(AudioSegment.from_mp3(audio).duration_seconds))

    audio = voice_over('Приглашаем вас в наш телеграмм-канал "Книжный Шкаф". Там вы наайдёте ещё больше обзоров книг, цитат из них и много чего интересного. До встречи!')
    audio_sequence.append(audio)
    video_sequence.append(demo_clip(AudioSegment.from_mp3(audio).duration_seconds))

    composite_audio()
    composite_video()

    os.system('ffmpeg -y -i Source\\Wish.mp3 -filter:a "volume=0.1" temp\\back_music.mp3 > temp\\null')
    os.system('ffmpeg -y -i temp\\audio.mp3 -i temp\\back_music.mp3 -shortest -filter_complex amerge=inputs=2 -ac 2 temp\\composed_audio_quit.mp3 > temp\\null')
    os.system('ffmpeg -y -i temp\\composed_audio_quit.mp3 -filter:a "volume=2" temp\\composed_audio.mp3 > temp\\null')
    os.system('ffmpeg -y -i temp\\video.mp4 -i temp\\composed_audio.mp3 -shortest -c copy -map 0:v:0 -map 1:a:0 temp\\output.mp4 > temp\\null')

    return 'temp\\output.mp4'



# start_clip: VideoClip = VideoFileClip('Source\\FinalVideos\\telegram.gif', has_mask=True).resize(height=625)
# start_clip.write_gif(f'temp\\new_tg.gif', pix_fmt='rgba', program='ffmpeg', tempfiles=True)

# print(AudioSegment.from_mp3('temp\\6629ff350fb09118393179.mp3').frame_rate)

# make_video(search_book('Сказать жизни "Да!": Психолог в концлагере'), 'Книга "Сказать жизни Да!" Виктора Франкла рассматривает опыт психолога, прошедшего концлагеря, и его последующие размышления о смысле жизни, практике логотерапии и психологической адаптации к экстремальным условиям. Она подойдет тем, кто интересуется аспектами психологии выживания, ищет вдохновение в реальных историях с пропитанным гуманизмом и надеждой. Несмотря на противоречивые впечатления от книги, она может вызвать интерес и вдохновить задуматься о смысле жизни.')

# make_video(search_book(url='https://livelib.ru/book/1008421858-zamok-broudi-archibald-kronin'), 'Книга "Замок Броуди" Джеймса Броуди рассказывает историю о семье, в которой царит тирания и деспотизм главы семейства, а их дом становится настоящей тюрьмой. Роман рассматривает тему семейных отношений, домашнего насилия и влияния токсичных отношений на судьбы членов семьи. Книга подойдет тем, кто ценит глубокое и эмоциональное повествование, а также заинтересован в психологических аспектах межличностных отношений.')

# os.system('ffmpeg -i temp\\output_quit.mp4 -filter:v "setpts=PTS/" output.mp4')

# make_video(search_book('Кафе на краю земли'), 'Книга "Кафе на краю земли" Джона Стрелеки рассказывает о путешествии главного героя. Эта книга подойдет тем, кто ищет вдохновение. Читатели оставили противоречивые отзывы.')

# os.system('ffmpeg -i Source\\TrackTribe.mp3 -i temp\\output.mp4 -filter_complex "[0:a][1:a]amerge,pan=stereo|c0<c0+c2|c1<c1+c3[a]" -map 1:v -map "[a]" -c:v copy -c:a aac -shortest temp\\output2.mp4')
# os.system('ffmpeg.exe -i temp\\video.mp4 -i temp\\audio.mp3 -filter_complex "[1:0]volume=0.2[a1];[0:a][a1]amix=inputs=2:duration=first" -map 0:v:0 temp\\out.mp4')
# os.system('ffmpeg -i  -i  -c copy -map 0:v:0 -map 1:a:0 temp\\output2.mp3')