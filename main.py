import os
from youtube.youtube_searcher import search_youtube
from downloader.audio_downloader import download_audio

MAX_RESULTS = 3  # Cambia este número para limitar la cantidad de vídeos a procesar

def main():
    personaje = input("Introduce el nombre del personaje: ")

    print("🔍 Buscando vídeos relacionados...")
    resultados = search_youtube(personaje, max_results=MAX_RESULTS)

    audios_descargados = []

    for resultado in resultados:
        url = resultado["url"]
        print(f"🎬 Procesando: {resultado['title']}")

        # Descargar audio en wav
        audio_path = download_audio(url)
        
        if not audio_path:
            print("❌ No se pudo descargar el audio.")
            continue

        audios_descargados.append(audio_path)

    print("✅ Todos los audios han sido descargados.")
    print("Audios disponibles para el siguiente paso:")
    for audio_file in audios_descargados:
        print(f" - {audio_file}")

    # Aquí iría el siguiente paso, pasando la lista completa:
    # diarize_and_transcribe(audios_descargados)

if __name__ == "__main__":
    main()
