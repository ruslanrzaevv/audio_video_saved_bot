# import os
# import requests
# import aiohttp
# from aiogram import Router, F
# from aiogram.filters import Command, CommandStart
# from aiogram.types import Message, FSInputFile
# from yt_dlp import YoutubeDL




# user_router = Router()

# def get_video_audio(url):
#     headers = {
#   "x-rapidapi-key": "7a421d13e5msh5e059dd06af3145p1c470ejsn83f2e2d8c3e4",
#   "x-rapidapi-host": "tiktok-video-no-watermark2.p.rapidapi.com/",
#     }
    
#     params = {'url':url, 'hd':1}

#     response = requests.get("https://tiktok-video-no-watermark2.p.rapidapi.com/", headers=headers, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         print(data)
#         video_url = data['data'].get('play', '')
#         audio_url = data['data'].get('music', '')
#         return video_url, audio_url
#     else:
#         print(f'Error: {response.status_code}')
#     return None, None

# @user_router.message(CommandStart())
# async def cmd_start(message: Message):
#     await message.reply('Welocme to bot')
    

# @user_router.message()
# async def send_media(message: Message):
#     url = message.text.strip()

#     if not url.startswith(('http://', 'https://')):
#         await message.answer('Пожалуйста, отправь корректную ссылку.')
#         return
    
#     await message.answer('⏳ Обрабатываю видео...')

    
#     video_url, audio_url = get_video_audio(url)
#     print(f"Video URLllllllllllllllllllllllllllhelo: {video_url}, Audio URL: {audio_url}")
    
#     video_path = 'video.mp4'
#     audio_path = 'audio.mp3'


#     try:
#         if video_url:
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(video_url) as video_response:
#                     with open(video_path, 'wb') as f:
#                         f.write(await video_response.read())

#             await message.answer('🎬 Отправляю видео...')
#             await message.answer_video(FSInputFile(video_path))

        
#         if audio_path:
#             async with aiohttp.ClientSession() as session:
#                 async with session.get(audio_url) as audio_response:
#                     with open(audio_path, 'wb') as f:
#                         f.write(await audio_response.read())     
                        
#             await message.answer('🎵 Отправляю аудио...')       
#             await message.answer_audio(FSInputFile(audio_path))

        
#         if not video_path and not audio_path:
#             await message.answer('Ошибка при обработке видео. Попробуй другую ссылку.')
        
#     except Exception as e:
#         await message.answer(f'Произошла ошибка: {e}')
    
#     finally:
#         if os.path.exists(video_path):
#             os.remove(video_path)
#         if os.path.exists(audio_path):
#             os.remove(audio_path)




 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
import hashlib
import requests
import os
import yt_dlp
from aiogram.types import FSInputFile
from aiogram.types import Message
from aiogram.types import BufferedInputFile

from db.database import save_video_info, get_video_info
from utils.convert import convert_m4a_to_mp3

DOWNLOAD_PATH = 'downloads'






def generate_url_id(url: str):
    return hashlib.md5(url.encode()).hexdigest()



def download_tiktok_video_audio(url):
    cached = get_video_info(url)
    if cached:
        return cached[0], cached[1]

    
    headers = {
        "x-rapidapi-key": "7a421d13e5msh5e059dd06af3145p1c470ejsn83f2e2d8c3e4",
        "x-rapidapi-host": "tiktok-video-no-watermark2.p.rapidapi.com",
    }
    
    params = {'url':url, 'hd':1}

    response = requests.get("https://tiktok-video-no-watermark2.p.rapidapi.com/", headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        # print(data)
        video_url = data['data'].get('play', '')
        audio_url = data['data'].get('music', '')
        
        if video_url:
            response = requests.get(video_url)  
            video_content = response.content            
            video_filename = f'{DOWNLOAD_PATH}/{generate_url_id(url)}.mp4'
            os.makedirs(DOWNLOAD_PATH, exist_ok=True)

            with open(video_filename, 'wb') as f:
                f.write(video_content)
        else:
            video_filename = None

        if audio_url:
            response = requests.get(audio_url)  
            audio_content = response.content
            audio_filename = f'{DOWNLOAD_PATH/{generate_url_id(url)}}.mp3'
            with open(audio_filename, 'wb') as f:
                f.write(audio_content)
        else:
            video_ = None
        return video_filename, audio_filename
    else:
        print(f'Error: {response.status_code}')
    return None, None



async def download_and_send(bot, chat_id, url, media_type):
    video_filename = None
    audio_filename = None

    # Если это TikTok
    if 'tiktok.com' in url:
        cached = get_video_info(url)
        if cached:
            video_filename, audio_filename = cached
        else:
            video_filename, audio_filename = download_tiktok_video_audio(url)
            if video_filename:
                save_video_info(url, video_filename, audio_filename)

        if video_filename:
            with open(video_filename, 'rb') as video_file:
                input_video = BufferedInputFile(video_file.read(), filename=os.path.basename(video_filename))
                await bot.send_video(chat_id, input_video, caption='Вот ваше видео без водяных знаков!')

            if audio_filename:
                with open(audio_filename, 'rb') as audio_file:
                    input_audio = BufferedInputFile(audio_file.read(), filename=os.path.basename(audio_filename))
                    await bot.send_audio(chat_id, input_audio, caption='Вот ваше аудио без водяных знаков!')

            # Удаляем только если не из кэша
            if not cached:
                os.remove(video_filename)
                if audio_filename:
                    os.remove(audio_filename)
        else:
            await bot.send_message(chat_id, 'Не удалось скачать видео или аудио с TikTok.')

    # Если это YouTube или другая платформа
    else:
        ydl_opts = {}

        if media_type == 'video':
            ydl_opts = {
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
            cached = get_video_info(url)
            if cached:
                video_filename, audio_filename = cached
                filename = video_filename or audio_filename
            else:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    filename = ydl.prepare_filename(info)

                    if media_type == 'audio':
                        filename = os.path.splitext(filename)[0] + '.mp3'

                    # Для универсальности
                    if media_type == 'video':
                        video_filename, audio_filename = filename, None
                    else:
                        video_filename, audio_filename = None, filename

                    save_video_info(url, video_filename, audio_filename)

            # Отправляем медиа
            if media_type == 'video' and video_filename:
                with open(video_filename, 'rb') as video_file:
                    input_video = BufferedInputFile(video_file.read(), filename=os.path.basename(video_filename))
                    await bot.send_video(chat_id, input_video, caption='Вот ваше видео!')

            elif media_type == 'audio' and audio_filename:
                if audio_filename.endswith('.m4a'):
                    mp3_file = convert_m4a_to_mp3(audio_filename)
                    if mp3_file:
                        await bot.send_audio(chat_id, FSInputFile(mp3_file))
                        os.remove(mp3_file)
                    else:
                        await bot.send_audio(chat_id, FSInputFile(audio_filename))
                else:
                    await bot.send_audio(chat_id, FSInputFile(audio_filename))

            # Удаляем только если не из кэша
            if not cached:
                if filename and os.path.exists(filename):
                    os.remove(filename)

        except Exception as e:
            await bot.send_message(chat_id, f'Ошибка: {e}')
        


   