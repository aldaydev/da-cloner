import os
import json
from qa_generator.qa_generator import generar_dataset_qa
from detecting.detecting import detect_roles_from_file

# Implementación local para lista de archivos
def detect_roles_from_files(file_paths, personaje):
    resultados = {}
    for file_path in file_paths:
        resultados[file_path] = detect_roles_from_file(file_path, personaje)
    return resultados

personaje = "Javier González Recuenco"
transcription_files = ["transcriptions/audio-test_transcription.json"]

# Detectar roles en las transcripciones
def add_roles_to_jsons(transcription_files, personaje):
    roles = detect_roles_from_files(transcription_files, personaje)
    archivos_validos = []
    for f in transcription_files:
        role_info = roles.get(f, {})
        interviewer = role_info.get("interviewer")
        interviewee = role_info.get("interviewee")
        if interviewer and interviewee:
            with open(f, "r", encoding="utf-8") as file_in:
                data = json.load(file_in)
            data["interviewer"] = interviewer
            data["interviewee"] = interviewee
            with open(f, "w", encoding="utf-8") as file_out:
                json.dump(data, file_out, ensure_ascii=False, indent=2)
            archivos_validos.append(f)
    return archivos_validos

archivos_validos = add_roles_to_jsons(transcription_files, personaje)

if archivos_validos:
    print("\n🚀 Generando dataset Q&A solo con transcripciones válidas...")
    output_path = generar_dataset_qa(archivos_validos, personaje)
    print(f"\n✅ Proceso completo. Dataset generado en: {output_path}")
else:
    print("⚠️ No se identificó entrevistador/entrevistado en ninguna transcripción.")
