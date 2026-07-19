from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"status": "server is running"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    return jsonify({"success": True, "token": "demo-token-123"})


@app.route("/upload", methods=["GET"])
def upload_page():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    audio_file = request.files.get("audio_file")
    return jsonify({"success": True, "file_id": "demo-file-1", "original_filename": "example.wav"})


@app.route("/clean", methods=["POST"])
def clean():
    return jsonify({
        "duration_sec": 42.3,
        "sample_rate": 16000,
        "silence_trimmed_sec": 8.1,
        "file_url": "/files/cleaned_001.wav"
    })


@app.route("/enroll", methods=["POST"])
def enroll():
    speaker_name = request.form.get("speaker_name")
    audio_file = request.files.get("audio_file")
    return jsonify({"success": True, "speaker_name": speaker_name, "samples_count": 1})


@app.route("/identify", methods=["POST"])
def identify():
    return jsonify({
        "segments": [
            {"start": 0.0, "end": 12.4, "speaker": "speaker_A", "confidence": 0.87},
            {"start": 12.4, "end": 30.1, "speaker": "unknown", "confidence": 0.31}
        ]
    })


@app.route("/report", methods=["POST"])
def report():
    return jsonify({
        "total_speakers": 2,
        "total_duration_sec": 42.3,
        "speaker_breakdown": {"speaker_A": 12.4, "unknown": 17.7}
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)
