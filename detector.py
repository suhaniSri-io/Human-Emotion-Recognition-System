import cv2

from deepface import DeepFace

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

camera = None
latest_emotion = "Detecting..."

emotion_stats = {
"happy": 0,
"sad": 0,
"angry": 0,
"neutral": 0,
"surprise": 0,
"fear": 0,
"disgust": 0
}

# ---------------- LIVE CAMERA ----------------
def generate_frames():
    global latest_emotion

    while True:
        success, frame = camera.read()
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face = frame[y:y+h, x:x+w]

            try:
                result = DeepFace.analyze(
                    face,
                    actions=['emotion'],
                    enforce_detection=False
                )

                emotion = result[0]['dominant_emotion']
                latest_emotion = emotion
                if emotion in emotion_stats:
                    emotion_stats[emotion] += 1


                cv2.putText(
                    frame,
                    emotion,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

            except Exception:
                pass

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame +
            b'\r\n'
        )
# ---------------- IMAGE EMOTION ----------------
def detect_emotion_image(path):
    try:
        result = DeepFace.analyze(img_path=path, actions=['emotion'], enforce_detection=False)
        return result[0]['dominant_emotion']
    except:
        return "No face detected"