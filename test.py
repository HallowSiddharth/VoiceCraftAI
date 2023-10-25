# from flask import Flask, request, jsonify, render_template

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('dubbing.html')

# @app.route('/update_language', methods=['POST'])
# def update_language():
#     data = request.get_json()
#     selected_language = data['language']
#     print(selected_language)
#     # Do something with the selected language (e.g., store it in a session)
    
#     return jsonify({'message': 'Language updated successfully'})

# if __name__ == '__main__':
#     app.run()

from transformers import pipeline
from pydub import AudioSegment
import os
from googletrans import Translator
from pytube import YouTube
import subprocess
from vtt_to_srt.vtt_to_srt import ConvertFile
from tqdm import tqdm
import sys
voice_names = {
    'tamil': 'ta-IN-ValluvarNeural',
    'kannada': 'kn-IN-GaganNeural',
    'telugu': 'te-IN-MohanNeural',
    'hindi': 'hi-IN-MadhurNeural',
}
final_output = "final"
languages = list(voice_names.keys())
for lang in languages:
    ffmpeg_command1 = ["ffmpeg", "-i", f"video_files/{lang}_f.mp4", "-vf", f"subtitles=srt_files/{lang}.srt:force_style='FontName=Arial,FontSize=13'", "-c:a", "copy", f"{final_output}/output_{lang}.mp4"]
    subprocess.run(ffmpeg_command1)