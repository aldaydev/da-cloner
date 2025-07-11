import os
import glob

def clean_audios_folder(folder='audios'):
    # Construimos la ruta para todos los mp3 en la carpeta indicada
    pattern = os.path.join(folder, '*.mp3')
    archivos = glob.glob(pattern)
    
    if not archivos:
        print(f"No hay archivos mp3 para borrar en la carpeta '{folder}'.")
        return
    
    for archivo in archivos:
        try:
            os.remove(archivo)
            print(f"Archivo borrado: {archivo}")
        except Exception as e:
            print(f"No se pudo borrar {archivo}: {e}")

if __name__ == '__main__':
    clean_audios_folder()
