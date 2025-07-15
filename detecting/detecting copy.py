# Para ejecutarlo aislado: python detecting/detecting.py transcriptions/audio-test_transcription.json "Javier González"

import json
from collections import defaultdict
import sys

def detect_roles_from_file(file_path, personaje):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Adaptar la estructura: convertir JSON complejo a lista plana de bloques
    if isinstance(data, dict) and "speakers" in data:
        bloques = []
        for speaker_data in data["speakers"]:
            speaker_name = speaker_data.get("speaker", "Unknown")
            for segment in speaker_data.get("segments", []):
                bloques.append({
                    "speaker": speaker_name,
                    "text": segment.get("text", "")
                })
        
    else:
        print("❌ Error: El JSON debe ser una lista de bloques con 'speaker' y 'text'.")
        sys.exit(1)

    speakers = get_speakers(bloques)
    speakers_count = len(speakers)
    if speakers_count > 2:
        print(f"⚠️ Se detectaron {speakers_count} hablantes. Solo se admite análisis con máximo 2.")
        return {
            "interviewer": None,
            "interviewee": None
        }

    name_variants = generar_variantes_de_nombre(personaje)

    more_words = get_more_words(bloques)
    more_questions = get_more_questions(bloques)
    interpellate = get_interpellate(bloques, name_variants)
    welcome_speaker = get_welcome_speaker(bloques)

    print("DEBUG:")
    print("MORE_WORDS =>", more_words)
    print("MORE_QUESTIONS =>", more_questions)
    print("INTERPELLATE =>", interpellate)
    print("WELCOME_SPEAKER =>", welcome_speaker)

    # Lógica de inferencia

    #El caso más seguro
    if more_questions == interpellate and more_questions == welcome_speaker and more_words != more_questions:
        interviewer = more_questions
        interviewee = [s for s in speakers if s != interviewer][0]
        return {
            "interviewer": interviewer,
            "interviewee": interviewee
        }

    if more_questions == interpellate:
        interviewer = more_questions
        interviewee = [s for s in speakers if s != interviewer][0]
    elif more_questions == more_words:
        interviewer = more_questions
        interviewee = [s for s in speakers if s != interviewer][0]
    elif interpellate == more_words:
        interviewer = interpellate
        interviewee = [s for s in speakers if s != interviewer][0]
    else:
        interviewer = more_questions
        interviewee = [s for s in speakers if s != interviewer][0]

    return {
        "interviewer": interviewer,
        "interviewee": interviewee
    }

def get_speakers(bloques):
    return list({bloque["speaker"] for bloque in bloques})

def generar_variantes_de_nombre(nombre):
    partes = nombre.strip().lower().split()
    variantes = set()

    if not partes:
        return []

    for i in range(len(partes)):
        for j in range(i+1, len(partes)+1):
            variantes.add(" ".join(partes[i:j]))

    return list(variantes)

def get_more_words(bloques):
    palabras_por_speaker = defaultdict(int)
    for bloque in bloques:
        palabras_por_speaker[bloque["speaker"]] += len(bloque["text"].split())
    return max(palabras_por_speaker.items(), key=lambda x: x[1])[0]

def get_more_questions(bloques):
    preguntas_por_speaker = defaultdict(int)
    for bloque in bloques:
        preguntas_por_speaker[bloque["speaker"]] += bloque["text"].count("?")
    return max(preguntas_por_speaker.items(), key=lambda x: x[1])[0]

def get_interpellate(bloques, variantes_nombre):
    menciones = defaultdict(int)
    for bloque in bloques:
        texto = bloque["text"].lower()
        for variante in variantes_nombre:
            if variante in texto:
                menciones[bloque["speaker"]] += 1
    if menciones:
        return max(menciones.items(), key=lambda x: x[1])[0]
    else:
        return None

def get_welcome_speaker(bloques):
    for bloque in bloques:
        texto = bloque["text"].lower()
        if "bienvenido" in texto or "bienvenida" in texto:
            return bloque["speaker"]
    return None


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python detecting/detecting.py <ruta_al_json> <nombre_personaje>")
        print("Ejemplo: python detecting/detecting.py transcriptions/audio-test_transcription.json \"Javier González\"")
        sys.exit(1)

    file_path = sys.argv[1]
    personaje = sys.argv[2]

    resultado = detect_roles_from_file(file_path, personaje)

    print("\n🎯 Resultado:")
    print(f"🗣️ Entrevistador: {resultado['interviewer']}")
    print(f"🎤 Entrevistado: {resultado['interviewee']}")
