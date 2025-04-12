import hashlib
import ffmpeg
import requests
import os
import time
import yt_dlp
from aiogram.types import FSInputFile

DOWNLOAD_PATH = 'downloads'


def convert_m4a_to_mp3(m4a_path):
    mp3_path = m4a_path.replace('.m4a', 'mp3')
    try:
        (
            ffmpeg
            .input(m4a_path)
            .output(mp3_path, vcodec='libx264',acodec='aac', strict='experimental')
            .run(overwrite_output=True)
        )
        return mp3_path
    except Exception as e:
        print(f'[FFMPEG ERROR] {e}')
        return None

def generate_url_id(url: str):
    return hashlib.md5(url.encode()).hexdigest()

async def download_and_send(bot, chat_id, url, media_type):
    filename = None
    media_file = media_type.strip().lower()
    if media_type == 'video':

        ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'downloads/%(title)s.{"mp4" if media_type == "video" else "m4a"}',
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
        start_time = time.time()

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            # print(f'Formats:{info['formats']}')
            filename = ydl.prepare_filename(info)
            
            if media_type == 'audio':
                filename = os.path.splitext(filename)[0] + '.mp3'

        eplased_time = time.time() - start_time
        
        media_file = FSInputFile(filename)
        
        if media_type == 'video':
            await bot.send_video(chat_id, media_file, caption=f'Video, timeout:{eplased_time:.2f}')
        else:
            if filename.endswith('.m4a'):
                mp3_file = convert_m4a_to_mp3(filename)
                if mp3_file:
                    await bot.send_audio(chat_id, FSInputFile(mp3_file), caption=f'Audio, timeout:{eplased_time:.2f}')
                    os.remove(mp3_file)
                else:
                    await bot.send_audio(chat_id, media_file, caption=f'Audio, timeout:{eplased_time:.2f}')
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

