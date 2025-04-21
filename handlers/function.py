import hashlib
import ffmpeg
import requests
import os
import time
import yt_dlp
from aiogram.types import FSInputFile
from aiogram.types import Message
from aiogram.types import BufferedInputFile

from utils.convert import convert_m4a_to_mp3

DOWNLOAD_PATH = 'downloads'



def generate_url_id(url: str):
    return hashlib.md5(url.encode()).hexdigest()



import hashlib
import os
import requests

DOWNLOAD_PATH = 'downloads'

RAPIDAPI_HOST = 'tiktok-video-no-watermark2.p.rapidapi.com'

def generate_url_id(url: str):
    return hashlib.md5(url.encode()).hexdigest()


# def download_tiktok_video(url):
    
#     headers = {
#         "x-rapidapi-key": "7a421d13e5msh5e059dd06af3145p1c470ejsn83f2e2d8c3e4",
#         "x-rapidapi-host": RAPIDAPI_HOST,
#     }
    

#     # Параметры запроса
#     params = {
#         'url': url
#     }

#     # Выполняем запрос к API
#     response = requests.get(f'https://{RAPIDAPI_HOST}/download', headers=headers, params=params)

#     if response.status_code == 200:
#         video_url = response.json().get('video_url')
#         video_content = requests.get(video_url).content

#         # Сохраняем видео
#         video_file = 'tiktok_video.mp4'
#         with open(video_file, 'wb') as f:
#             f.write(video_content)

#         return video_file
#     else:
#         return None



def download_tiktok_video_audio(url):
    headers = {
        "x-rapidapi-key": "7a421d13e5msh5e059dd06af3145p1c470ejsn83f2e2d8c3e4",
        "x-rapidapi-host": "tiktok-video-no-watermark2.p.rapidapi.com",
    }
    
    params = {'url': url, 'hd': 1}
    response = requests.get("https://tiktok-video-no-watermark2.p.rapidapi.com/", headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        print(data)
        video_url = data['data'].get('play', '')
        audio_url = data['data'].get('music', '')

        video_filename = None
        if video_url:
            response = requests.get(video_url)  
            video_content = response.content            
            video_filename = f'{DOWNLOAD_PATH}/{generate_url_id(url)}.mp4'
            os.makedirs(DOWNLOAD_PATH, exist_ok=True)
            with open(video_filename, 'wb') as f:
                f.write(video_content)

        audio_filename = None
        if audio_url:
            response = requests.get(audio_url)  
            audio_content = response.content
            audio_filename = f'{DOWNLOAD_PATH}/{generate_url_id(url)}.mp3'
            with open(audio_filename, 'wb') as f:
                f.write(audio_content)

        return video_filename, audio_filename
    else:
        print(f'Error: {response.status_code}')
    return None, None

def download_youtube_video_audio(url, media_type):
    if media_type == 'video':
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': 'downloads/%(title).100s.%(ext)s',
            'sanitize_filename': True,
        }
    elif media_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

            if media_type == 'audio':
                filename = os.path.splitext(filename)[0] + '.mp3'

            return filename
    except Exception as e:
        print(f'Error downloading from YouTube: {e}')
        return None


async def download_and_send(bot, chat_id, url, media_type):
    filename = None

    if 'tiktok.com' in url:
        video_filename, audio_filename = download_tiktok_video_audio(url)
        
        if video_filename:
            with open(video_filename, 'rb') as video_file:
                video_data = video_file.read()
                input_video = BufferedInputFile(video_data, filename=video_filename)
                await bot.send_video(chat_id, input_video, caption='Вот ваше видео без водяных знаков!')
            
            if audio_filename:
                with open(audio_filename, 'rb') as audio_file:
                    audio_data = audio_file.read()
                    input_audio = BufferedInputFile(audio_data, filename=audio_filename)
                    await bot.send_audio(chat_id, input_audio, caption='Вот ваше аудио без водяных знаков!')
            
            os.remove(video_filename)
            if audio_filename:
                os.remove(audio_filename)
        else:
            await bot.send_message(chat_id, 'Не удалось скачать видео или аудио с TikTok.')

    elif 'youtube.com' in url:
        # Для YouTube используем функцию для скачивания видео или аудио
        filename = download_youtube_video_audio(url, media_type)
        
        if filename:
            media_file = FSInputFile(filename)
            if media_type == 'video':
                with open(filename, 'rb') as video_file:
                    video_data = video_file.read()
                    input_video = BufferedInputFile(video_data, filename='video.mp4')
                    await bot.send_video(chat_id, input_video, caption='Вот ваше видео!')

            else:
                if filename.endswith('.m4a'):
                    mp3_file = convert_m4a_to_mp3(filename)
                    if mp3_file:
                        await bot.send_audio(chat_id, FSInputFile(mp3_file))
                        os.remove(mp3_file)
                    else:
                        await bot.send_audio(chat_id, media_file)
                else:
                    await bot.send_audio(chat_id, media_file)

            os.remove(filename)
        else:
            await bot.send_message(chat_id, 'Не удалось скачать видео или аудио с YouTube.')

    else:
        await bot.send_message(chat_id, 'Неподдерживаемый источник для скачивания.')
