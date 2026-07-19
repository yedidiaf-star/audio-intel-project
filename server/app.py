from flask import Flask, request, jsonify, render_template

from tasks.task_01_login import login_agent
from tasks.task_02_upload import handle_upload
# from tasks.task_03_cleaning import clean_audio
# from tasks.task_04_enrollment import enroll_speaker
# from tasks.task_06_segmentation import segment_and_identify
# from tasks.task_07_report import build_report

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"status": "server is running"})


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    result = login_agent(data.get("username"), data.get("password"))
    return jsonify(result)


@app.route("/upload", methods=["GET"])
def upload_page():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload():
    audio_file = request.files.get("audio_file")
    result = handle_upload(audio_file)
    return jsonify(result)


@app.route("/clean", methods=["POST"])
def clean():
    data = request.json
    result = clean_audio(data.get("file_id"))
    return jsonify(result)


@app.route("/enroll", methods=["POST"])
def enroll():
    speaker_name = request.form.get("speaker_name")
    audio_file = request.files.get("audio_file")
    result = enroll_speaker(speaker_name, audio_file)
    return jsonify(result)


@app.route("/identify", methods=["POST"])
def identify():
    data = request.json
    result = segment_and_identify(data.get("file_url"))
    return jsonify(result)


@app.route("/report", methods=["POST"])
def report():
    data = request.json
    result = build_report(data.get("segments"))
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
