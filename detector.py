from deepface import DeepFace

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

def detect_emotion_image(path):
    try:
        result = DeepFace.analyze(
            img_path=path,
            actions=['emotion'],
            enforce_detection=False
        )
        return result[0]['dominant_emotion']

    except Exception:
        return "No face detected"