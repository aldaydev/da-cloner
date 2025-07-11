import yt_dlp

def descargar_audio(url, carpeta_salida):
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': f'{carpeta_salida}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': r'downloader\ffmpeg\bin'  # <-- aquí pones la ruta relativa
    }
    
    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    url_prueba = 'https://www.youtube.com/watch?v=YFnzhXt3fFc'
    carpeta = 'audios'
    descargar_audio(url_prueba, carpeta)
