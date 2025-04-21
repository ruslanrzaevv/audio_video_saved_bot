import ffmpeg

def convert_m4a_to_mp3(m4a_path):
    mp3_path = m4a_path.replace('.m4a', 'mp3')
    try:
        (
            ffmpeg
            .input(m4a_path)
            .output(mp3_path, acodec='libmp3lame', audio_bitrate='192k')
            .run(overwrite_output=True)
        )
        return mp3_path
    except Exception as e:
        print(f'[FFMPEG ERROR] {e}')
        return None