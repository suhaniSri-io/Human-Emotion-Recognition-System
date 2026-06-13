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
        from deepface import DeepFace

        result = DeepFace.analyze(
            img_path=path,
            actions=['emotion'],
            enforce_detection=False
        )
        emotion = result[0].get('dominant_emotion', 'No face detected')
        region = result[0].get('region')
        return {
            'emotion': emotion,
            'region': region
        }

    except Exception:
        return {
            'emotion': 'No face detected',
            'region': None
        }
