from tqdm import tqdm
from transformers import pipeline
from pydub import AudioSegment
import os
from googletrans import Translator
import subprocess


text_directory = "text_files"
if not os.path.exists(text_directory):
    os.makedirs(text_directory)


voice_names = {
    'kannada': 'kn-IN-GaganNeural',
    'hindi' : 'hi-IN-MadhurNeural',
    'tamil' : 'ta-IN-ValluvarNeural',
    'malayalam' : 'ml-IN-MidhunNeural',
    'telugu' : 'te-IN-MohanNeural', 
    'bengali' : 'bn-IN-BashkarNeural',
    'gujarati' : 'gu-IN-NiranjanNeural',
    'marathi' : 'mr-IN-ManoharNeural',
    'urdu' : 'ur-IN-SalmanNeural'


}

languages = list(voice_names.keys())  

translator = Translator()

abspath = f"/home/a/voicecraft/demo/VoiceCraftAI/"
output_directory = abspath + "vtt files"
srt_directory = abspath + "srt_files"
text_directory = abspath+ "text_files"
video_directory = abspath+"video_files"
audio_directory = abspath+"audio_files"
final_output = abspath+"final"

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

def transcribe(languages):
    languages = languages
    print("Transcribing:")
    abspath = f"/home/a/voicecraft/demo/VoiceCraftAI/"
    whisper = pipeline("automatic-speech-recognition", model="openai/whisper-medium")

    ffmpeg_command = [
        "ffmpeg",
        "-y", 
        "-i",
        "/home/a/voicecraft/demo/VoiceCraftAI/demo.mp4",
        "/home/a/voicecraft/demo/VoiceCraftAI/english.mp3"
    ]
    subprocess.run(ffmpeg_command)

    audio_file = abspath+"english.mp3"

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

    with open(os.path.join(text_directory, "english.txt"), "w") as f:
        f.write(full_transcript)

    translate(languages,full_transcript)


def translate(languages, full_transcript):
    abspath = f"/home/a/voicecraft/demo/VoiceCraftAI/"
    for lang in languages:
        translated = translator.translate(text=full_transcript, src="en", dest=lang)
        translated_text = translated.text
        with open(f'{text_directory}/{lang}.txt', 'w+', encoding='utf-8') as f:
            f.write(translated_text)
    
        tts_command = ["edge-tts", "--voice", f"{voice_names[lang]}", "--text", f"{translated_text}", "--write-media", f"{audio_directory}/{lang}.mp3", "--write-subtitles", f"{output_directory}/{lang}.vtt"]
        subprocess.run(tts_command)

        input_video = abspath +"demo.mp4"
        input_audio = os.path.join(audio_directory, f"{lang}.mp3")
        output_video = os.path.join(video_directory, f"{lang}.mp4")
        ffmpeg_command = [
                "ffmpeg",
                "-y",
                "-i",
                input_video,
                "-i",
                input_audio,
                "-c:v", "copy",
                "-af", "atempo=1.1",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-strict", "experimental",
            "-map", "0:v", 
            "-map", "1:a",
                output_video,
            ]
        subprocess.run(ffmpeg_command)

if __name__ == "__main__":
    full_transcript = transcribe()