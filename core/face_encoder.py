import os
import numpy as np
import face_recognition

def generar_encoding(ruta_foto: str) -> str:
    """
    Genera el encoding del rostro en una imagen y lo guarda en /data/encodings/.
    
    Args:
        ruta_foto (str): Ruta de la imagen capturada.
    
    Returns:
        str: Ruta del archivo .npy con el encoding.
    
    Raises:
        Exception: Si no se detecta un rostro, si hay más de uno 
                   o si no se puede generar el encoding.
    """

    if not os.path.exists(ruta_foto):
        raise Exception(f"La foto no existe: {ruta_foto}")

    # Cargar la imagen
    imagen = face_recognition.load_image_file(ruta_foto)

    # Detectar rostros
    ubicaciones = face_recognition.face_locations(imagen)

    if len(ubicaciones) == 0:
        raise Exception("No se detectó ningún rostro en la foto.")
    if len(ubicaciones) > 1:
        raise Exception("La foto contiene más de un rostro. Intenta de nuevo.")

    # Obtener encoding
    encodings = face_recognition.face_encodings(imagen, known_face_locations=ubicaciones)

    if len(encodings) == 0:
        raise Exception("No se pudo generar el encoding del rostro.")

    encoding = encodings[0]

    # Directorio de salida
    output_dir = os.path.join("data", "encodings")
    os.makedirs(output_dir, exist_ok=True)

    # Nombre del archivo .npy
    nombre_archivo = os.path.splitext(os.path.basename(ruta_foto))[0] + ".npy"
    ruta_encoding = os.path.join(output_dir, nombre_archivo)

    # Guardar encoding como numpy
    np.save(ruta_encoding, encoding)

    print(f"[INFO] Encoding guardado en: {ruta_encoding}")

    return ruta_encoding
