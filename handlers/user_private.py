import os
import requests
import aiohttp
from aiogram import Router, F
from aiogram.filters import CommandStart, Filter
from aiogram.types import Message, FSInputFile, URLInputFile

import kbds.inline_kb as in_kb
import handlers.function as hf
from handlers.function import generate_url_id
import url_storage as storage   
from handlers.function import download_tiktok_video_audio

user_router = Router()


@user_router.message(CommandStart())
async def cmd_start(message:Message):
    await message.answer('😮‍💨Привет, отправь ссылку на видео Instagram, Facebook, TikTok, YuoTube и я отправлю видео без водяных знаков!😎')

class LinkFilter(Filter):
    async def __call__(self, message: Message):
        return message.text.startswith('http')

# @user_router.message(LinkFilter())
# async def link_handler(message: Message):
#     link = message.text

#     msg = await message.answer('Обрабатываю видео')
#     url = "https://tiktok-video-no-watermark2.p.rapidapi.com/comment/reply"

#     querystring = {"video_id":"7093219391759764782","comment_id":"7093219663211053829","count":"10","cursor":"0"}

#     headers = {
#         "x-rapidapi-key": "f226ceb580mshbc0e0e8d1670b92p1f43f4jsn4c89715242ec",
#         "x-rapidapi-host": "tiktok-video-no-watermark2.p.rapidapi.com"
#     }

#     response = requests.get(url, headers=headers, params=querystring)
#     print(response.status_code)
#     print(response.text)  
#     video_link = None  

#     try:
#         video_link = response.json()['data']['play']
#     except KeyError:
#         await msg.edit_text('Ссылка оказалась неверной ')
    
#     if video_link:
#         await msg.edit_text('Отправляю видео...')
#         await msg.delete()
#         await message.answer_video(URLInputFile(video_link))
#     else:
#         await msg.edit_text('Не удалось получить видео.')
        

@user_router.message()
async def send_media(message: Message):
    url = message.text.strip()

    if not url.startswith(('http://', 'https://')):
        await message.answer('Пожалуйста, отправь корректную ссылку.')
        return

    if 'tiktok.com' in url:
        video_filename, audio_filename = download_tiktok_video_audio(url)
        if video_filename:
            url_id = hf.generate_url_id(url)
            storage.url_storage[url_id] = url
            storage.save_url_storage(storage.url_storage)
            storage.url_storage = storage.load_url_storage()
            await message.answer('Выбери формат:', reply_markup=await in_kb.format_btn(url_id))  
        else:
            await message.answer('Не удалось получить видео или аудио с TikTok.')

    else:
        
        url_id = hf.generate_url_id(url)
        storage.url_storage[url_id] = url
        storage.save_url_storage(storage.url_storage)
        storage.url_storage = storage.load_url_storage()
        await message.answer('Выбери формат:', reply_markup=await in_kb.format_btn(url_id))