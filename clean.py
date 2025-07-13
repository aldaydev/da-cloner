import os
import glob

def clean_folder(folder):
    pattern = os.path.join(folder, '*')  # Todos los archivos en la carpeta
    archivos = glob.glob(pattern)
    
    if not archivos:
        print(f"No hay archivos para borrar en la carpeta '{folder}'.")
        return
    
    for archivo in archivos:
        nombre_archivo = os.path.basename(archivo)
        
        # Saltar archivos que no queremos eliminar
        if nombre_archivo in ['.gitkeep', 'audio-test.wav']:
            print(f"Saltando archivo: {archivo}")
            continue
        
        try:
            os.remove(archivo)
            print(f"Archivo borrado: {archivo}")
        except Exception as e:
            print(f"No se pudo borrar {archivo}: {e}")

if __name__ == '__main__':
    clean_folder('audios')
