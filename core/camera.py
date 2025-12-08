import cv2
import os
from datetime import datetime

def capturar_foto(nombre_archivo: str) -> str:
    """
    Abre la webcam, captura una foto cuando el usuario presiona ESPACIO
    y la guarda en /data/faces/.
    
    Retorna la ruta final de la foto guardada.

    Raises:
        Exception si no se puede acceder a la cámara o guardar la foto.
    """

    # Directorio donde se guardarán las fotos
    output_dir = os.path.join("data", "faces")
    os.makedirs(output_dir, exist_ok=True)

    # Iniciar webcam
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        raise Exception("No se pudo acceder a la cámara.")

    print("[INFO] Presiona ESPACIO para capturar la foto. Presiona ESC para cancelar.")

    while True:
        ret, frame = cam.read()

        if not ret:
            cam.release()
            raise Exception("Error al leer la cámara.")

        # Mostrar vista previa
        cv2.imshow("Captura - Presiona ESPACIO", frame)

        key = cv2.waitKey(1) & 0xFF

        # Si presiona espacio → capturar foto
        if key == 32:  # Tecla espacio
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{nombre_archivo}_{timestamp}.jpg"
            ruta_final = os.path.join(output_dir, filename)

            cv2.imwrite(ruta_final, frame)

            cam.release()
            cv2.destroyAllWindows()

            print(f"[INFO] Foto guardada en: {ruta_final}")
            return ruta_final

        # ESC para salir sin capturar
        if key == 27:
            cam.release()
            cv2.destroyAllWindows()
            raise Exception("Captura cancelada por el usuario.")
