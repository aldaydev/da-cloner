import os
from youtube.youtube_searcher import search_youtube
from downloader.audio_downloader import download_audio
from transcriber.transcriber import diarize_and_transcribe
from qa_generator.qa_generator import generar_dataset_qa
from detecting.detecting import detect_roles_from_file

# Implementación local para lista de archivos
def detect_roles_from_files(file_paths, personaje):
    resultados = {}
    for file_path in file_paths:
        resultados[file_path] = detect_roles_from_file(file_path, personaje)
    return resultados
from dotenv import load_dotenv

load_dotenv()

MAX_RESULTS = 1  # Número máximo de vídeos a buscar

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

    DURACION_MINIMA_SEGUNDOS = 6200  # 2 horas
    duracion_total = sum(video["duration_seconds"] for video in videos)

    if duracion_total < DURACION_MINIMA_SEGUNDOS:
        minutos = int(duracion_total // 60)
        print(f"\n❌ No hay suficiente contenido público sobre esa persona ({minutos} minutos encontrados).")
        return

    print(f"\n🎧 Descargando audios de {len(videos)} vídeos...")
    audio_paths = []
    metadata_list = []

    for video in videos:
        print(f"\n🎬 Título: {video['title']}")
        print(f"🔗 URL: {video['url']}")

        audio_path = download_audio(video['url'])

        if audio_path:
            print(f"✅ Audio descargado: {audio_path}")
            audio_paths.append(audio_path)
            # Guardamos metadatos para este audio
            metadata_list.append({
                "personaje": personaje,
                "title": video["title"],
                "url": video["url"]
            })
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

    # Pasamos también metadata_list a la función
    transcription_files = diarize_and_transcribe(audio_paths, hf_token, metadata_list)

    if transcription_files:
        print("\n📁 Transcripciones generadas:")
        for f in transcription_files:
            print(f" - {f}")

        # Detectar roles en las transcripciones
        roles = detect_roles_from_files(transcription_files, personaje)
        archivos_validos = []
        for f in transcription_files:
            role_info = roles.get(f, {})
            interviewer = role_info.get("interviewer")
            interviewee = role_info.get("interviewee")
            if interviewer and interviewee:
                # Añadir los campos al JSON de la transcripción
                with open(f, "r", encoding="utf-8") as file_in:
                    data = json.load(file_in)
                data["interviewer"] = interviewer
                data["interviewee"] = interviewee
                with open(f, "w", encoding="utf-8") as file_out:
                    json.dump(data, file_out, ensure_ascii=False, indent=2)
                archivos_validos.append(f)

        if archivos_validos:
            print("\n🚀 Generando dataset Q&A solo con transcripciones válidas...")
            output_path = generar_dataset_qa(archivos_validos, personaje)
            print(f"\n✅ Proceso completo. Dataset generado en: {output_path}")
        else:
            print("⚠️ No se identificó entrevistador/entrevistado en ninguna transcripción.")
    else:
        print("⚠️ No se generaron transcripciones.")

if __name__ == "__main__":
    main()
