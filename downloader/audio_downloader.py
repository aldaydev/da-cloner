import os
import yt_dlp

def download_audio(url, output_folder='audios'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    options = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': 'downloader/ffmpeg/bin',  # Ruta relativa
        'quiet': False,
        'no_warnings': True
    }
    
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])