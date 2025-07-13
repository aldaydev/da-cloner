import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
import isodate  # Para parsear duración en formato ISO 8601

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def search_youtube(query, max_results=5):
    # 🔍 Enriquecer el término de búsqueda
    enriched_query = f'"{query}" entrevista OR conferencia OR charla OR ponencia OR podcast'

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
    
    search_response = youtube.search().list(
        q=enriched_query,
        part="id",
        maxResults=max_results,
        type="video"
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]

    if not video_ids:
        return []

    # Obtener detalles adicionales con videos().list
    video_response = youtube.videos().list(
        part="snippet,contentDetails",
        id=",".join(video_ids)
    ).execute()

    videos = []
    for item in video_response.get("items", []):
        video_id = item["id"]
        snippet = item["snippet"]
        content_details = item["contentDetails"]

        title = snippet["title"]
        description = snippet.get("description", "")
        tags = snippet.get("tags", [])
        channel = snippet.get("channelTitle", "")
        duration = isodate.parse_duration(content_details["duration"]).total_seconds()

        # Filtro: solo incluir vídeos de al menos 5 minutos
        if duration < 300:
            continue

        url = f"https://www.youtube.com/watch?v={video_id}"

        videos.append({
            "title": title,
            "url": url,
            "description": description,
            "tags": tags,
            "channel": channel,
            "duration_seconds": duration
        })


    return videos


if __name__ == "__main__":
    query = "Javier González Recuenco"
    results = youtube_search(query)

    for video in results:
        print(f"🎬 {video['title']}")
        print(f"🔗 {video['url']}")
        print(f"📺 Canal: {video['channel']}")
        print(f"⏱ Duración: {video['duration_seconds']:.0f} segundos")
        print(f"🏷 Tags: {video['tags']}")
        print(f"📝 Descripción: {video['description'][:100]}...\n")
