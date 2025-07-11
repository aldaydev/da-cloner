from youtube.youtube_searcher import youtube_search
from downloader.audio_downloader import download_audio

def main():
    query = input("🔍 Introduce el nombre de la persona o tema: ").strip()
    if not query:
        print("⚠️ No introdujiste una búsqueda.")
        return

    max_results = 5
    print("\n🔎 Buscando vídeos en YouTube...\n")
    videos = youtube_search(query, max_results)

    if not videos:
        print("❌ No se encontraron vídeos.")
        return

    print(f"\n📋 Se encontraron {len(videos)} vídeos:\n")
    for i, video in enumerate(videos, 1):
        print(f"{i}. {video['title']}\n   {video['url']}\n")

    confirm = input("¿Quieres descargar el audio de estos vídeos? (s/n): ").strip().lower()
    if confirm != 's':
        print("❌ Descarga cancelada.")
        return

    print("\n⬇️ Iniciando descarga de audios...\n")
    for i, video in enumerate(videos, 1):
        print(f"{i}. Descargando: {video['title']}")
        download_audio(video["url"])
    print("\n✅ Descargas completadas.")

if __name__ == "__main__":
    main()