# v3
from transformers import pipeline
from pydub import AudioSegment
import os
from googletrans import Translator
from pytube import YouTube
import subprocess
from vtt_to_srt.vtt_to_srt import ConvertFile
from tqdm import tqdm
import sys

url = "https://www.youtube.com/watch?v=oO2qQNLSDnM&ab_channel=CIPAMIndia"

whisper = pipeline("automatic-speech-recognition", model="openai/whisper-medium")

directory = r"E:\ha"

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

print(full_transcript)

voice_names = {
    'tamil': 'ta-IN-ValluvarNeural',
    'kannada': 'kn-IN-GaganNeural',
    'telugu': 'te-IN-MohanNeural',
    'hindi': 'hi-IN-MadhurNeural',
    'bengali' : 'bn-BD-PradeepNeural',
    'gujarati' : 'gu-IN-NiranjanNeural',
    'malayalam' : 'ml-IN-MidhunNeural',
    'marathi' : 'mr-IN-ManoharNeural',
    'urdu' : 'ur-IN-SalmanNeural'
}

languages = list(voice_names.keys())  
# full_transcript = 'In a world filled with diversity, we strive for unity, embracing the beauty of our differences.'

translator = Translator()

output_directory = "vtt files"
srt_directory = "srt_files"
text_directory = "text_files"
video_directory = "video_files"
audio_directory = "audio_files"
final_output = "final"

if not os.path.exists(output_directory):
    os.makedirs(output_directory)

if not os.path.exists(srt_directory):
    os.makedirs(srt_directory)

if not os.path.exists(text_directory):
    os.makedirs(text_directory)

if not os.path.exists(video_directory):
    os.makedirs(video_directory)

if not os.path.exists(audio_directory):
    os.makedirs(audio_directory)

if not os.path.exists(final_output):
    os.makedirs(final_output)

for lang in languages:
    translated = translator.translate(text=full_transcript, src="en", dest=lang)
    translated_text = translated.text
    with open(f'{text_directory}/{lang}.txt', 'w+', encoding='utf-8') as f:
        f.write(translated_text)
    
    tts_command = ["edge-tts", "--voice", f"{voice_names[lang]}", "--text", f"{translated_text}", "--write-media", f"{audio_directory}/{lang}.mp3", "--write-subtitles", f"{output_directory}/s{lang}.vtt"]
    subprocess.run(tts_command)

    input_video = "demo.mp4"
    input_audio = f"{audio_directory}\{lang}.mp3"
    output_video = f"video_files\{lang}_f.mp4"
    ffmpeg_command = [
            "ffmpeg",
            "-y",
            "-i",
            input_video,
            "-i",
            input_audio,
            "-c:v", "copy",
            # "-vf", r"subtitles='E:\GITHUB Repo\VoiceCraftAI\tamil.srt',scale=1280:720",
            "-af", "atempo=1.1",
        "-c:v", "libx264",
        "-c:a", "aac",
        "-strict", "experimental",
        "-map", "0:v", 
        "-map", "1:a",
            output_video,
        ]
    subprocess.run(ffmpeg_command)
    # with open(f'{text_directory}/{lang}.txt', 'r', encoding='utf-8') as f , open(f'{srt_directory}/{lang}.srt', 'w+', encoding='utf-8') as f1:
    #     a = f.read()
    #     b = a.split()
    #     w = 0
    #     q = '00:00:00,100 --> 00:00:03,737'
    #     set = 1
    #     s = ''
    #     for i in b:
    #         s += i + ' '
    #         w += 1
    #         if lang != 'hindi':
    #             if w == 4:
    #                 f1.write(str(set) + '\n' + q + '\n' +s + '\n')
    #                 set += 1
    #                 s = ''
    #                 w = 0
    #                 t = list(q)
    #                 t[7] = str(int(t[7]) + 3)
    #                 t[24] = str(int(t[24]) + 3)
    #                 q = "".join(t)
    #         else:
    #             if w == 12:
    #                 f1.write(str(set) + '\n' + q + '\n' +s + '\n')
    #                 set += 1
    #                 s = ''
    #                 w = 0
    #                 t = list(q)
    #                 t[7] = str(int(t[7]) + 3)
    #                 t[24] = str(int(t[24]) + 3)
    #                 q = "".join(t)
    #     if s:
    #         f1.write(s)
    # ffmpeg_command1 = ["ffmpeg", "-i", f"video_files/{lang}_f.mp4", "-vf", f"subtitles=srt_files/{lang}.srt:force_style='FontName=Arial,FontSize=13'", "-c:a", "copy", f"{final_output}/output_{lang}.mp4"]
    # subprocess.run(ffmpeg_command1)