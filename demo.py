# from transformers import pipeline

# whisper = pipeline("automatic-speech-recognition", model="openai/whisper-medium")
# text = whisper(r"E:\code\hackathon\test.mp3")
# print(text)
# from transformers import pipeline

# # Initialize the ASR pipeline
# whisper = pipeline("automatic-speech-recognition", model="openai/whisper-medium")

# # Define the audio file path
# audio_file = r"E:\code\hackathon\test2.mp3"

# # Initialize variables to store the results
# full_transcript = ""

# # Set the chunk size (in seconds)
# chunk_size = 30

# # Open the audio file
# with open(audio_file, "rb") as f:
#     # Read the audio file in chunks
#     while True:
#         chunk = f.read(
#             chunk_size * 1000
#         )  # Read a chunk of data (30 seconds in this case)
#         if not chunk:
#             break  # If the chunk is empty, we've reached the end of the file
#         # Perform ASR on the chunk and append the result to the full transcript
#         chunk_transcript = whisper(chunk)
#         print(chunk_transcript["text"])
#         full_transcript += chunk_transcript["text"]

# # Print the full transcript
# print(full_transcript)

# v3
from transformers import pipeline
from pydub import AudioSegment
import os
from googletrans import Translator
from pytube import YouTube
import subprocess
from tqdm import tqdm
import sys

# args = sys.argv
# url = args[0]

url = "https://www.youtube.com/watch?v=oO2qQNLSDnM&ab_channel=CIPAMIndia"

# Initialize the ASR pipeline
whisper = pipeline("automatic-speech-recognition", model="openai/whisper-medium")

# download the video and convert the audio

directory = r"E:\GITHUB Repo\VoiceCraftAI"

ffmpeg_command = [
    "ffmpeg",
    "-y",  # Add the -y flag here to force overwrite
    "-i",
    "demo.mp4",
    "english.mp3"
]
subprocess.run(ffmpeg_command)

# Define the audio file path
audio_file = "english.mp3"

# Set the chunk size (in milliseconds)
chunk_size_ms = 30000  # 30 seconds

# Create a directory to store the audio chunk files
output_dir = "audio_chunks"
os.makedirs(output_dir, exist_ok=True)

# Open the audio file
audio = AudioSegment.from_file(audio_file)

# Initialize variables to store the results
full_transcript = ""

# Split the audio into chunks and process each chunk
for i, start_time in enumerate(tqdm(range(0, len(audio), chunk_size_ms),desc="PROGRESSING : ")):
    chunk = audio[start_time : start_time + chunk_size_ms]
    chunk_path = os.path.join(output_dir, f"chunk_{i}.wav")
    chunk.export(chunk_path, format="wav")
    chunk_transcript = whisper(chunk_path)
    full_transcript += chunk_transcript["text"]

# Clean up: remove the temporary audio chunk files
for i in range(len(os.listdir(output_dir))):
    os.remove(os.path.join(output_dir, f"chunk_{i}.wav"))

# Print the full transcript
print(full_transcript)

translator = Translator()
translated = translator.translate(text=full_transcript, src="en", dest="ta")
tamil = translated.text

translated = translator.translate(text=full_transcript, src="en", dest="kn")
kannada = translated.text

translated = translator.translate(text=full_transcript, src="en", dest="hi")
hindi = translated.text


translated = translator.translate(text=full_transcript, src="en", dest="te")
telugu = translated.text


tts_command = ["edge-tts", "--voice", "ta-IN-ValluvarNeural", f"--text", f"{tamil}", "--write-media", "tamil.mp3", "--write-subtitles", "stamil.srt"]
subprocess.run(tts_command)
tts_command = ["edge-tts", "--voice", "hi-IN-MadhurNeural", f"--text", f"{hindi}", "--write-media", "hindi.mp3", "--write-subtitles", "shindi.srt"]
subprocess.run(tts_command)
tts_command = ["edge-tts", "--voice", "te-IN-MohanNeural", f"--text", f"{telugu}", "--write-media", "telugu.mp3", "--write-subtitles", "stelugu.srt"]
subprocess.run(tts_command)
tts_command = ["edge-tts", "--voice", "kn-IN-GaganNeural", f"--text", f"{kannada}", "--write-media", "kannada.mp3", "--write-subtitles", "skannada.srt"]
subprocess.run(tts_command)

input_video = "demo.mp4"
output_video = r"E:\GITHUB Repo\VoiceCraftAI\tamil_f.mp4"
input_audio = "tamil.mp3"
ffmpeg_command = [
        "ffmpeg",
        "-y",  # Add the -y flag here to force overwrite
        "-i",
        input_video,
        "-i",
        input_audio,
        "-c:v", "copy",
        "-vf", r"subtitles='E:\GITHUB Repo\VoiceCraftAI\tamil.srt',scale=1280:720",
        "-af", "atempo=1.1",
    "-c:v", "libx264",
    "-c:a", "aac",
    "-strict", "experimental",
    "-map", "0:v",  # Map the video stream from input_video
    "-map", "1:a",
        output_video,
    ]
subprocess.run(ffmpeg_command)
output_video = r"E:\GITHUB Repo\VoiceCraftAI\telugu_f.mp4"
input_audio = "telugu.mp3"
ffmpeg_command = [
        "ffmpeg",
        "-y",  # Add the -y flag here to force overwrite
        "-i",
        input_video,
        "-i",
        input_audio,
        "-c:v", "copy",
        "-vf", r"subtitles='E:\GITHUB Repo\VoiceCraftAI\telugu.srt',scale=1280:720",
        "-af", "atempo=1.1",
    "-c:v", "libx264",
    "-c:a", "aac",
    "-strict", "experimental",
    "-map", "0:v",  # Map the video stream from input_video
    "-map", "1:a",
        output_video,
    ]
subprocess.run(ffmpeg_command)
output_video = r"E:\GITHUB Repo\VoiceCraftAI\hindi_f.mp4"
input_audio = "hindi.mp3"
ffmpeg_command = [
        "ffmpeg",
        "-y",  # Add the -y flag here to force overwrite
        "-i",
        input_video,
        "-i",
        input_audio,
        "-c:v", "copy",
        "-vf", r"subtitles='E:\GITHUB Repo\VoiceCraftAI\hindi.srt',scale=1280:720",
        "-af", "atempo=1.1",
    "-c:v", "libx264",
    "-c:a", "aac",
    "-strict", "experimental",
    "-map", "0:v",  # Map the video stream from input_video
    "-map", "1:a",
        output_video,
    ]
subprocess.run(ffmpeg_command)
output_video = r"E:\GITHUB Repo\VoiceCraftAI\kannada_f.mp4"
input_audio = "kannada.mp3"
ffmpeg_command = [
        "ffmpeg",
        "-y",  # Add the -y flag here to force overwrite
        "-i",
        input_video,
        "-i",
        input_audio,
        "-c:v", "copy",
        "-vf", r"subtitles='E:\GITHUB Repo\VoiceCraftAI\kannada.srt',scale=1280:720",
        "-af", "atempo=1.1",
    "-c:v", "libx264",
    "-c:a", "aac",
    "-strict", "experimental",
    "-map", "0:v",  # Map the video stream from input_video
    "-map", "1:a",
        output_video,
    ]
subprocess.run(ffmpeg_command)