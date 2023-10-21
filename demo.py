from transformers import pipeline
from pydub import AudioSegment
import os
from googletrans import Translator
from pytube import YouTube
import subprocess
from vtt_to_srt.vtt_to_srt import ConvertFile
from tqdm import tqdm
from moviepy.editor import *
import sys

text_directory = "text_files"
if not os.path.exists(text_directory):
    os.makedirs(text_directory)

voice_names = {
    'tamil': 'ta-IN-ValluvarNeural',
    'kannada': 'kn-IN-GaganNeural',
    'telugu': 'te-IN-MohanNeural',
    'hindi': 'hi-IN-MadhurNeural'
}

languages = list(voice_names.keys()) 

def transcribe(url):

    whisper = pipeline("automatic-speech-recognition", model="openai/whisper-medium")

    # directory = r"E:\ha"

    yt = YouTube(url)
    video = yt.streams.get_highest_resolution()
    video.download()
    video_title = yt.title
    current_file_name = f"{video_title}.mp4"
    new_file_name = "demo.mp4"

    if os.path.exists(current_file_name):
        os.rename(current_file_name, new_file_name)
        print(f"File '{current_file_name}' has been renamed to '{new_file_name}'.")
    else:
        print(f"File '{current_file_name}' does not exist.")

    ffmpeg_command = [
        "ffmpeg",
        "-y", 
        "-i",
        "demo.mp4",
        "english.mp3"
    ]
    subprocess.run(ffmpeg_command)

    audio_file = "english.mp3"

    chunk_size_ms = 30000 

    output_dir = "audio_chunks"
    os.makedirs(output_dir, exist_ok=True)

    audio = AudioSegment.from_file(audio_file)

    full_transcript = ""

    for i, start_time in enumerate(tqdm(range(0, len(audio), chunk_size_ms),desc="PROGRESSING : ")):
        chunk = audio[start_time : start_time + chunk_size_ms]
        chunk_path = os.path.join(output_dir, f"chunk_{i}.wav")
        chunk.export(chunk_path, format="wav")
        chunk_transcript = whisper(chunk_path)
        full_transcript += chunk_transcript["text"]

    for i in range(len(os.listdir(output_dir))):
        os.remove(os.path.join(output_dir, f"chunk_{i}.wav"))

    return full_transcript

def translate(full_transcript):

    translator = Translator()

    for lang in languages:
        translated = translator.translate(text=full_transcript, src="en", dest=lang)
        translated_text = translated.text
        with open(f'{text_directory}/{lang}.txt', 'w+', encoding='utf-8') as f:
            f.write(translated_text)
    
    return 'True'

url = "https://youtu.be/MeBt-1F9nZo?si=cak78p186KVbo8xg"

yt = YouTube(url)