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

            speakers = data.get("speakers", [])
            if len(speakers) != 2:
                continue  # Solo procesamos entrevistas con 2 speakers

            # Asumimos que SPEAKER_00 es entrevistador y SPEAKER_01 es entrevistado
            preguntas = [seg["text"].strip() for seg in speakers[0]["segments"] if "?" in seg["text"]]
            respuestas = [seg["text"].strip() for seg in speakers[1]["segments"]]

            # Emparejamos cada pregunta con la siguiente respuesta disponible
            for pregunta, respuesta in zip(preguntas, respuestas):
                if len(pregunta.split()) < 3 or len(respuesta.split()) < 5:
                    continue  # ignoramos pares muy cortos
                conversacion = [
                    system_prompt,
                    {"role": "user", "content": pregunta},
                    {"role": "assistant", "content": respuesta}
                ]
                out_file.write(json.dumps({"messages": conversacion}, ensure_ascii=False) + "\n")
                total_pares += 1

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
