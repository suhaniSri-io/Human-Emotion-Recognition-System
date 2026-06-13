from flask import Flask, render_template, request, redirect, url_for, session
from detector import detect_emotion_image
import detector
import base64
app = Flask(__name__)
app.secret_key = "emotion_ai_secret"

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "admin" and password == "1234":
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return render_template("login.html", error="Invalid Credentials")

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# ---------------- HOME ----------------
@app.route('/')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")


# ---------------- IMAGE UPLOAD PAGE ----------------
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('login'))

    emotion = None

    if request.method == 'POST':
        file = request.files['image']
        path = "static/upload.jpg"
        file.save(path)

        emotion = detect_emotion_image(path)

    return render_template("upload.html", emotion=emotion)

# ---------------- LIVE EMOTION API ----------------
@app.route('/live_emotion')
def live_emotion():
    return {"emotion": detector.latest_emotion}


#-----------Analytics API----------------
@app.route('/emotion_stats')
def emotion_stats():
    return detector.emotion_stats

@app.route('/reset_stats', methods=['POST'])
def reset_stats():
    if 'user' not in session:
        return redirect(url_for('login'))

    for key in detector.emotion_stats:
        detector.emotion_stats[key] = 0
    detector.latest_emotion = "Detecting..."
    return {"success": True}

@app.route('/detect_frame', methods=['POST'])
def detect_frame():
    try:
        data = request.json['image']

        # Remove base64 header
        image_data = data.split(',')[1]
        image_bytes = base64.b64decode(image_data)

        path = "static/upload.jpg"
        with open(path, "wb") as f:
            f.write(image_bytes)

        result = detect_emotion_image(path)
        emotion = result.get('emotion')
        region = result.get('region')
        detector.latest_emotion = emotion

        if emotion in detector.emotion_stats:
            detector.emotion_stats[emotion] += 1

        response = {
            "success": True,
            "emotion": emotion
        }

        if region:
            response["region"] = region

        return response

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    app.run(debug=True)