import hashlib
import requests
import os
import time
import yt_dlp
from aiogram.types import FSInputFile

def generate_url_id(url: str):
    return hashlib.md5(url.encode()).hexdigest()

async def download_and_send(bot, chat_id, url, media_type):
    ydl_options = {
   'format': 'bestaudio[ext=m4a]/bestvideo[ext=mp4]/best',
    'outtmpl': f'downloads/%(title)s.{"mp4" if media_type == "video" else "m4a"}',
    }


    try:
        start_time = time.time()

        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(url, download=True)
            # print(f'Formats:{info['formats']}')
            filename = ydl.prepare_filename(info)

        end_time = time.time()
        eplased_time = end_time - start_time
        
        media_file = FSInputFile(filename)
        if media_type == 'video':
            await bot.send_video(chat_id, media_file, caption=f'Video, timeout:{eplased_time:.2f}')
        else:
            await bot.send_audio(chat_id, media_file, caption=f'Audio, timeout:{eplased_time:.2f}')

        
        os.remove(filename)

    except Exception as e:
        await bot.send_message(chat_id, f'Error:{e}')
        


def get_video_audio(url):
    headers = {
  "x-rapidapi-key": "7a421d13e5msh5e059dd06af3145p1c470ejsn83f2e2d8c3e4",
  "x-rapidapi-host": "tiktok-video-no-watermark2.p.rapidapi.com/",
    }
    
    params = {'url':url, 'hd':1}

    response = requests.get("https://tiktok-video-no-watermark2.p.rapidapi.com/", headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        print(data)
        video_url = data['data'].get('play', '')
        audio_url = data['data'].get('music', '')
        return video_url, audio_url
    else:
        print(f'Error: {response.status_code}')
    return None, None