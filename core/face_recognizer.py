import cv2
import numpy as np
import face_recognition
from database.queries import obtener_todos_los_encodings

TOLERANCE = 0.5


def cargar_encodings():
    """
    Carga todos los encodings desde la base de datos.
    Retorna:
        encodings (list[np.array])
        persona_ids (list[int])
    """
    datos = obtener_todos_los_encodings()

    encodings = []
    persona_ids = []

    for persona_id, ruta_encoding in datos:
        try:
            encoding = np.load(ruta_encoding)
            encodings.append(encoding)
            persona_ids.append(persona_id)
        except Exception as e:
            print(f"[WARN] No se pudo cargar encoding {ruta_encoding}: {e}")

    return encodings, persona_ids


def iniciar_reconocimiento():
    """
    Inicia la cámara y reconoce rostros en tiempo real.
    """
    known_encodings, persona_ids = cargar_encodings()

    if not known_encodings:
        raise Exception("No hay encodings registrados en el sistema.")

    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        raise Exception("No se pudo acceder a la cámara.")

    print("[INFO] Reconocimiento iniciado. Presiona ESC para salir.")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        # Convertir BGR (OpenCV) a RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detectar rostros y encodings en el frame
        locations = face_recognition.face_locations(rgb_frame)
        encodings_frame = face_recognition.face_encodings(rgb_frame, locations)

        for (top, right, bottom, left), face_encoding in zip(locations, encodings_frame):

            # Comparar con encodings conocidos
            distances = face_recognition.face_distance(known_encodings, face_encoding)
            min_distance = np.min(distances)

            if min_distance < TOLERANCE:
                match_index = np.argmin(distances)
                persona_id = persona_ids[match_index]
                label = f"ID {persona_id}"
                color = (0, 255, 0)
            else:
                label = "Desconocido"
                color = (0, 0, 255)

            # Dibujar bounding box y nombre
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(
                frame,
                label,
                (left, top - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                color,
                2
            )

        cv2.imshow("Reconocimiento Facial", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cam.release()
    cv2.destroyAllWindows()
