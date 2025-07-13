from faster_whisper import WhisperModel
from pyannote.audio import Pipeline
import os
import json
from dotenv import load_dotenv

load_dotenv()

def diarize_and_transcribe(audio_paths, hf_token):
    # Cargar modelo Whisper
    model = WhisperModel("medium", device="cpu", compute_type="int8")

    # Cargar pipeline de diarización
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                        use_auth_token=hf_token)

    output_files = []

    for path in audio_paths:
        print(f"\n🎧 Procesando archivo: {path}")

        # Aplicar diarización
        diarization = pipeline(path)

        print("🔊 Diarización:")
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            print(f"🗣️ {speaker}: [{turn.start:.1f}s - {turn.end:.1f}s]")

        print("\n📝 Transcripción:")
        segments, _ = model.transcribe(path, vad_filter=True, language="es")
        segments = list(segments)  # convertir generator a lista

        print(f"Total segmentos transcritos: {len(segments)}")
        for segment in segments:
            print(f"[{segment.start:.1f}s - {segment.end:.1f}s] {segment.text.strip()}")

        # --- Cruzar diarización con transcripción ---

        speaker_texts = {}
        turns = []
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            turns.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker
            })

        for segment in segments:
            seg_start = segment.start
            seg_end = segment.end
            seg_text = segment.text.strip()

            max_overlap = 0
            assigned_speaker = None

            for turn in turns:
                overlap_start = max(seg_start, turn["start"])
                overlap_end = min(seg_end, turn["end"])
                overlap = max(0, overlap_end - overlap_start)

                if overlap > max_overlap:
                    max_overlap = overlap
                    assigned_speaker = turn["speaker"]

            if assigned_speaker is None:
                assigned_speaker = "unknown"

            print(f"Segmento [{seg_start:.2f}s - {seg_end:.2f}s] asignado a speaker: {assigned_speaker} (overlap {max_overlap:.2f}s)")

            if assigned_speaker not in speaker_texts:
                speaker_texts[assigned_speaker] = []

            speaker_texts[assigned_speaker].append({
                "start": seg_start,
                "end": seg_end,
                "text": seg_text
            })

        transcription_data = {
            "audio_file": path,
            "speakers": []
        }

        for speaker, segments_list in speaker_texts.items():
            transcription_data["speakers"].append({
                "speaker": speaker,
                "segments": segments_list
            })

        base_name = os.path.splitext(os.path.basename(path))[0]
        output_dir = "transcriptions"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"{base_name}_transcription.json")

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(transcription_data, f, ensure_ascii=False, indent=2)

        print(f"✅ Transcripción guardada en {output_path}")
        output_files.append(output_path)

        print("\n" + "-" * 40)

    return output_files


if __name__ == "__main__":
    hf_token = os.environ.get("HUGGINGFACE_TOKEN")

    if not hf_token:
        print("❌ No se encontró la variable de entorno HUGGINGFACE_TOKEN.")
    else:
        default_audio = 'audios/audio-test.wav'
        if not os.path.exists(default_audio):
            print(f"❌ No se encontró el archivo {default_audio}")
        else:
            diarize_and_transcribe([default_audio], hf_token)
