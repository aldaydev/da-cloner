import os
import yt_dlp

def download_audio(url, output_folder='audios'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_template = f'{output_folder}/%(title)s.%(ext)s'

    options = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'ffmpeg_location': 'downloader/ffmpeg/bin',
        'quiet': False,
        'no_warnings': True,
        'noplaylist': True,
        'extract_flat': False,
        'cachedir': False
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)

            # Obtener la ruta real del archivo generado
            if 'requested_downloads' in info:
                for entry in info['requested_downloads']:
                    filepath = entry.get('filepath')
                    if filepath and os.path.exists(filepath):
                        return filepath

            # En caso alternativo, intentar construirla manualmente
            title = info.get('title')
            if title:
                filepath = os.path.join(output_folder, f"{title}.wav")
                if os.path.exists(filepath):
                    return filepath

    except Exception as e:
        print(f"❌ Error al descargar: {e}")

    return None

# --- MODO PRUEBA AISLADA ---
if __name__ == "__main__":
    ejemplos = [
        "https://youtu.be/NrDSEEcOW6Y?si=ios9mvn69kW2JGcS",  # Ejemplo Javier González Recuenco
        "https://youtu.be/oelb294jvGg?si=8SxsBhEjLu8zicAW"   # Puedes añadir más URLs aquí
    ]
    for url in ejemplos:
        print(f"\nDescargando audio de: {url}")
        resultado = download_audio(url)
        if resultado:
            print(f"✅ Audio descargado en: {resultado}")
        else:
            print("❌ Error en la descarga.")
