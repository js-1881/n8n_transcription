from flask import Flask, request, jsonify
import whisper
import subprocess
import os

app = Flask(__name__)

# Load the Whisper model
model = whisper.load_model("base")

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Save the file to a temporary location
    audio_path = "/tmp/uploaded_audio.mp3"
    file.save(audio_path)

    # Use FFmpeg to convert the audio if needed (e.g., to WAV format)
    converted_audio_path = "/tmp/converted_audio.wav"
    subprocess.run(['ffmpeg', '-i', audio_path, converted_audio_path])

    # Transcribe the audio using Whisper
    result = model.transcribe(converted_audio_path)

    return jsonify({'transcription': result['text']}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
