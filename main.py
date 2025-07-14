import os
from youtube.youtube_searcher import search_youtube
from downloader.audio_downloader import download_audio
from transcriber.transcriber import diarize_and_transcribe
from dotenv import load_dotenv

load_dotenv()

MAX_RESULTS = 3  # Número máximo de vídeos a buscar

def main():
    personaje = input("Introduce el nombre del personaje: ").strip()
    if not personaje:
        print("❌ Debes introducir un nombre.")
        return

    print(f"\n🔍 Buscando vídeos de YouTube sobre: {personaje}")
    videos = search_youtube(personaje, max_results=MAX_RESULTS)

    if not videos:
        print("❌ No se encontraron vídeos adecuados.")
        return

    print(f"\n🎧 Descargando audios de {len(videos)} vídeos...")
    audio_paths = []

    for video in videos:
        print(f"\n🎬 Título: {video['title']}")
        print(f"🔗 URL: {video['url']}")

        audio_path = download_audio(video['url'])

        if audio_path:
            print(f"✅ Audio descargado: {audio_path}")
            audio_paths.append(audio_path)
        else:
            print("⚠️ Falló la descarga de este vídeo.")

    if not audio_paths:
        print("\n❌ No se pudo descargar ningún audio.")
        return

    print("\n📝 Transcribiendo y aplicando diarización...")
    hf_token = os.environ.get("HUGGINGFACE_TOKEN")

    if not hf_token:
        print("❌ Token de Hugging Face no encontrado. Verifica tu archivo .env.")
        return

    transcription_files = diarize_and_transcribe(audio_paths, hf_token)

    if transcription_files:
        print("\n📁 Transcripciones generadas:")
        for f in transcription_files:
            print(f" - {f}")
    else:
        print("⚠️ No se generaron transcripciones.")

if __name__ == "__main__":
    main()
