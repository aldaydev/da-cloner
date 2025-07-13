import os
import whisper
import json
import sys

def add_ffmpeg_to_path():
    ffmpeg_path = os.path.abspath("downloader/ffmpeg/bin")  # Cambia esta ruta
    if ffmpeg_path not in os.environ["PATH"]:
        os.environ["PATH"] = ffmpeg_path + os.pathsep + os.environ["PATH"]

# Justo antes de importar whisper o llamar a transcribe_audio:
add_ffmpeg_to_path()

# Ahora importas whisper o llamas a la función que usa ffmpeg

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)

    # Extraemos la información relevante con la estructura deseada
    data = {
        "file": os.path.basename(audio_path),
        "segments": [
            {
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            }
            for segment in result.get("segments", [])
        ],
        "text": result.get("text", "")
    }

    # Crear carpeta 'transcriptions' si no existe
    output_dir = "transcriptions"
    os.makedirs(output_dir, exist_ok=True)

    # Nombre archivo salida .json
    title = os.path.splitext(os.path.basename(audio_path))[0]
    output_path = os.path.join(output_dir, f"{title}.json")

    # Guardar json con indentación para lectura humana
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ Transcripción guardada en: {output_path}")
