import os
import requests
import aiohttp
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile

import kbds.inline_kb as in_kb
import handlers.function as hf
import url_storage as storage   
from handlers.function import get_video_audio

user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer('😮‍💨Привет, отправь ссылку на видео Instagram, Facebook, TikTok, YuoTube и я отправлю видео без водяных знаков!😎')

@user_router.message()
async def video_request(message: Message):
    url = message.text.strip()
    url_id = hf.generate_url_id(url)
    storage.url_storage[url_id] = url
    storage.save_url_storage(storage.url_storage)
    storage.url_storage =  storage.load_url_storage()
    await message.answer('Choose format:', reply_markup= await in_kb.format_btn(url_id))




#Tiktokkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk
@user_router.message()
async def send_media(message: Message):
    url = message.text.strip()

    if not url.startswith(('http://', 'https://')):
        await message.answer('Пожалуйста, отправь корректную ссылку.')
        return
    
    await message.answer('⏳ Обрабатываю видео...')

    
    video_url, audio_url = get_video_audio(url)
    print(f"\nVideo URL: {video_url}, Audio URL: {audio_url}")
    
    video_path = 'video.mp4'
    audio_path = 'audio.mp3'


    try:
        if video_url:
            async with aiohttp.ClientSession() as session:
                async with session.get(video_url) as video_response:
                    with open(video_path, 'wb') as f:
                        f.write(await video_response.read())

            await message.answer('🎬 Отправляю видео...')
            await message.answer_video(FSInputFile(video_path))

        
        if audio_path:
            async with aiohttp.ClientSession() as session:
                async with session.get(audio_url) as audio_response:
                    with open(audio_path, 'wb') as f:
                        f.write(await audio_response.read())     
                        
            await message.answer('🎵 Отправляю аудио...')       
            await message.answer_audio(FSInputFile(audio_path))

        
        if not video_path and not audio_path:
            await message.answer('Ошибка при обработке видео. Попробуй другую ссылку.')
        
    except Exception as e:
        await message.answer(f'Произошла ошибка: {e}')
    
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(audio_path):
            os.remove(audio_path)