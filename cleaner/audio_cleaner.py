import os
import librosa
import noisereduce as nr
import soundfile as sf
import numpy as np

INPUT_FOLDER = 'audios'
OUTPUT_FOLDER = os.path.join('audios', 'cleaned')

def clean_audio_file(filename):
    input_path = os.path.join(INPUT_FOLDER, filename)
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    try:
        # Cargar audio en estéreo si existe
        y, sr = librosa.load(input_path, sr=None, mono=False)

        # Si es estéreo (2 canales), promedia para conservar la señal en ambos
        if y.ndim == 2:
            y = np.mean(y, axis=0)

        # Extraer ruido de un fragmento corto al inicio (por ejemplo, primeros 0.5 segundos)
        noise_sample = y[:int(0.5 * sr)]  # medio segundo

        # Reducir ruido con muestra explícita
        reduced_noise = nr.reduce_noise(y=y, y_noise=noise_sample, sr=sr)

        os.makedirs(OUTPUT_FOLDER, exist_ok=True)
        sf.write(output_path, reduced_noise, sr)
        print(f"✔️ Audio limpio guardado: {output_path}")

        # Eliminar original solo si limpieza fue exitosa
        os.remove(input_path)
        print(f"🗑️ Archivo original eliminado: {input_path}")

    except Exception as e:
        print(f"❌ Error procesando {filename}: {e}")
