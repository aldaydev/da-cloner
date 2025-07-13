from faster_whisper import WhisperModel
from pyannote.audio import Pipeline
import os

def diarize_and_transcribe(audio_paths=None):
    # Leer el token de Hugging Face desde variable de entorno
    hf_token = os.environ.get("HUGGINGFACE_TOKEN")

    if not hf_token:
        print("❌ ERROR: La variable de entorno HUGGINGFACE_TOKEN no está definida.")
        return

    # Si no se especifica audio_paths, usar audio-test.wav por defecto
    if audio_paths is None:
        audio_paths = ['audios/audio-test.wav']

    # Cargar modelo Whisper
    model = WhisperModel("medium", device="cpu", compute_type="int8")

    # Cargar pipeline de diarización
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                        use_auth_token=hf_token)

    for path in audio_paths:
        print(f"\n🎧 Procesando archivo: {path}")

        # Aplicar diarización
        diarization = pipeline(path)

        # Mostrar segmentos de speakers
        print("🔊 Diarización:")
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            print(f"🗣️ {speaker}: [{turn.start:.1f}s - {turn.end:.1f}s]")

        # Transcripción
        print("\n📝 Transcripción:")
        segments, _ = model.transcribe(path, vad_filter=True)

        for segment in segments:
            print(f"[{segment.start:.1f}s - {segment.end:.1f}s] {segment.text.strip()}")

        print("\n" + "-" * 40)

# Permitir ejecución directa
if __name__ == '__main__':
    diarize_and_transcribe()
