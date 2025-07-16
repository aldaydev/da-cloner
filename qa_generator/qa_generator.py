import json
import os
import sys

def generar_system_prompt(personaje):
    return {
        "role": "system",
        "content": (
            f"Eres {personaje}. Debes responder preguntas con tu estilo habitual, "
            f"manteniendo tu tono, personalidad y forma de expresarte tal como lo harías en una conversación real. "
            f"Evita responder como una IA, responde como lo haría {personaje}."
        )
    }

def generar_dataset_qa(transcription_files, personaje):
    output_dir = "datasets"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{personaje.lower().replace(' ', '_')}_qa_dataset.jsonl")

    system_prompt = generar_system_prompt(personaje)
    total_pares = 0


    with open(output_path, "w", encoding="utf-8") as out_file:
        for transcription_path in transcription_files:
            with open(transcription_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Filtro: solo procesar si se ha identificado entrevistador y entrevistado
            interviewer = data.get("interviewer")
            interviewee = data.get("interviewee")
            if interviewer is not None and interviewee is not None:
                speakers = data.get("speakers", [])
                if len(speakers) != 2:
                    continue  # Solo procesamos entrevistas con 2 speakers

                # Crear una lista de todos los segmentos y ordenarlos por 'start'
                all_segments = []
                for speaker_data in speakers:
                    for seg in speaker_data["segments"]:
                        all_segments.append({
                            "speaker": speaker_data["speaker"],
                            "text": seg["text"].strip(),
                            "is_question": "?" in seg["text"] and speaker_data["speaker"] == interviewer,
                            "start": seg.get("start", 0)
                        })
                all_segments.sort(key=lambda x: x["start"])

                i = 0
                while i < len(all_segments):
                    seg = all_segments[i]
                    if seg["is_question"]:
                        pregunta = seg["text"]
                        respuesta_segmentos = []
                        j = i + 1
                        while j < len(all_segments):
                            if all_segments[j]["speaker"] == interviewee:
                                respuesta_segmentos.append(all_segments[j]["text"])
                            elif all_segments[j]["speaker"] == interviewer and all_segments[j]["is_question"]:
                                break
                            elif all_segments[j]["speaker"] == interviewer and not all_segments[j]["is_question"]:
                                # Si el entrevistador hace un comentario, lo ignoramos y seguimos buscando respuesta
                                pass
                            j += 1
                        respuesta = " ".join(respuesta_segmentos).strip()
                        print(f"\nPregunta: {pregunta}")
                        print(f"Respuesta generada: {respuesta}")
                        print(f"Longitud pregunta: {len(pregunta.split())} palabras, longitud respuesta: {len(respuesta.split())} palabras")
                        conversacion = [
                            system_prompt,
                            {"role": "user", "content": pregunta},
                            {"role": "assistant", "content": respuesta}
                        ]
                        out_file.write(json.dumps({"messages": conversacion}, ensure_ascii=False) + "\n")
                        total_pares += 1
                        i = j
                    else:
                        i += 1

    print(f"\n✅ Dataset generado en {output_path} con {total_pares} ejemplos Q&A.")
    return output_path

# --- MODO PRUEBA AISLADA ---
if __name__ == "__main__":
    personaje = sys.argv[1] if len(sys.argv) > 1 else "Personaje de Prueba"
    archivo_prueba = "transcriptions/audio-test_transcription.json"

    if not os.path.exists(archivo_prueba):
        print(f"❌ No se encontró el archivo de prueba en: {archivo_prueba}")
        sys.exit(1)

    generar_dataset_qa([archivo_prueba], personaje)
