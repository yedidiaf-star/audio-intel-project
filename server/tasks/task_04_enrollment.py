
import pathlib
import numpy as np
import librosa
import json
import librosa.feature

DB_PATH = pathlib.Path(__file__).resolve().parent.parent.parent / "data" / "speaker_profiles.json"



def enroll_speaker(speaker_name, file_path):
    try:
        y, sr = librosa.load(file_path, sr=None)

        mfcc_features = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)

        voice_vector = np.mean(mfcc_features.T, axis=0).tolist()

        db = load_speaker_profiles()

        if speaker_name not in db:
            db[speaker_name] = []

        db[speaker_name].append(voice_vector)

        with open(DB_PATH, "w") as file:
            json.dump(db, file)

        return {"success": True,"speaker_name": speaker_name,"samples_count": len(db[speaker_name])}

    except Exception as e:
        print(f"Error processing audio for {speaker_name}: {e}")
        return {"success": False, "error": "Invalid audio file or processing failed"}


def load_speaker_profiles():
    try:
        with open(DB_PATH, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}