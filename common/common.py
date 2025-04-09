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




    