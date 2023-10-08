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
from vtt_to_srt.vtt_to_srt import ConvertFile
from tqdm import tqdm
import sys

# args = sys.argv
# url = args[0]

url = "https://www.youtube.com/watch?v=oO2qQNLSDnM&ab_channel=CIPAMIndia"

# Initialize the ASR pipeline
whisper = pipeline("automatic-speech-recognition", model="openai/whisper-medium")

# download the video and convert the audio

directory = r"E:\ha"

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

voice_names = {
    'tamil': 'ta-IN-ValluvarNeural',
    'kannada': 'kn-IN-GaganNeural',
    'telugu': 'te-IN-MohanNeural',
    'hindi': 'hi-IN-MadhurNeural'
}

languages = list(voice_names.keys())  # Get the list of languages from the keys of the dictionary
full_transcript = 'In a world filled with diversity, we strive for unity, embracing the beauty of our differences.'

translator = Translator()

for lang in languages:
    translated = translator.translate(text=full_transcript, src="en", dest=lang)
    translated_text = translated.text
    with open(f'{lang}.txt', 'w+', encoding='utf-8') as f:
        f.write(translated_text)
    
    tts_command = ["edge-tts", "--voice", f"{voice_names[lang]}", "--text", f"{translated_text}", "--write-media", f"{lang}.mp3", "--write-subtitles", f"s{lang}.vtt"]
    subprocess.run(tts_command)

    input_video = "demo.mp4"
    base_path = r"E:\ha"
    # output_video = r"E:\ha\tamil_f.mp4"
    input_audio = f"{lang}.mp3"
    output_video = f"{base_path}/{lang}_f.mp4"
    ffmpeg_command = [
            "ffmpeg",
            "-y",  # Add the -y flag here to force overwrite
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
        "-map", "0:v",  # Map the video stream from input_video
        "-map", "1:a",
            output_video,
        ]
    subprocess.run(ffmpeg_command)
    with open(f'{lang}.txt', 'r', encoding='utf-8') as f , open(f'{lang}.srt', 'w+', encoding='utf-8') as f1:
        a = f.read()
        b = a.split()
        w = 0
        q = '00:00:00,100 --> 00:00:03,737'
        set = 1
        s = ''
        for i in b:
            s += i + ' '
            w += 1
            if lang != 'hindi':
                if w == 4:
                    f1.write(str(set) + '\n' + q + '\n' +s + '\n')
                    set += 1
                    s = ''
                    w = 0
                    t = list(q)
                    t[7] = str(int(t[7]) + 3)
                    t[24] = str(int(t[24]) + 3)
                    q = "".join(t)
            else:
                if w == 12:
                    f1.write(str(set) + '\n' + q + '\n' +s + '\n')
                    set += 1
                    s = ''
                    w = 0
                    t = list(q)
                    t[7] = str(int(t[7]) + 3)
                    t[24] = str(int(t[24]) + 3)
                    q = "".join(t)
        if s:
            f1.write(s)
    ffmpeg_command1 = ["ffmpeg", "-i", f"{lang}_f.mp4", "-vf", f"subtitles={lang}.srt:force_style='FontName=Arial,FontSize=13'", "-c:a", "copy", f"output_{lang}.mp4"]
    subprocess.run(ffmpeg_command1)

# translator = Translator()
# translated = translator.translate(text=full_transcript, src="en", dest="ta")
# tamil = translated.text

# translated = translator.translate(text=full_transcript, src="en", dest="kn")
# kannada = translated.text

# translated = translator.translate(text=full_transcript, src="en", dest="hi")
# hindi = translated.text

# translated = translator.translate(text=full_transcript, src="en", dest="te")
# telugu = translated.text


# tts_command = ["edge-tts", "--voice", "ta-IN-ValluvarNeural", "--text", f"{tamil}", "--write-media", "tamil.mp3", "--write-subtitles", "stamil.vtt"]
# subprocess.run(tts_command)
# tts_command = ["edge-tts", "--voice", "hi-IN-MadhurNeural", f"--text", f"{hindi}", "--write-media", "hindi.mp3", "--write-subtitles", "shindi.vtt"]
# subprocess.run(tts_command)
# tts_command = ["edge-tts", "--voice", "te-IN-MohanNeural", f"--text", f"{telugu}", "--write-media", "telugu.mp3", "--write-subtitles", "stelugu.vtt"]
# subprocess.run(tts_command)
# tts_command = ["edge-tts", "--voice", "kn-IN-GaganNeural", f"--text", f"{kannada}", "--write-media", "kannada.mp3", "--write-subtitles", "skannada.vtt"]
# subprocess.run(tts_command)

# input_video = "demo.mp4"
# output_video = r"E:\ha\tamil_f.mp4"
# input_audio = "tamil.mp3"
# ffmpeg_command = [
#         "ffmpeg",
#         "-y",  # Add the -y flag here to force overwrite
#         "-i",
#         input_video,
#         "-i",
#         input_audio,
#         "-c:v", "copy",
#         # "-vf", r"subtitles='E:\GITHUB Repo\VoiceCraftAI\tamil.srt',scale=1280:720",
#         "-af", "atempo=1.1",
#     "-c:v", "libx264",
#     "-c:a", "aac",
#     "-strict", "experimental",
#     "-map", "0:v",  # Map the video stream from input_video
#     "-map", "1:a",
#         output_video,
#     ]
# subprocess.run(ffmpeg_command)
# output_video = r"E:\ha\telugu_f.mp4"
# input_audio = "telugu.mp3"
# ffmpeg_command = [
#         "ffmpeg",
#         "-y",  # Add the -y flag here to force overwrite
#         "-i",
#         input_video,
#         "-i",
#         input_audio,
#         "-c:v", "copy",
#         # "-vf", r"subtitles='E:\GITHUB Repo\VoiceCraftAI\telugu.srt',scale=1280:720",
#         "-af", "atempo=1.1",
#     "-c:v", "libx264",
#     "-c:a", "aac",
#     "-strict", "experimental",
#     "-map", "0:v",  # Map the video stream from input_video
#     "-map", "1:a",
#         output_video,
#     ]
# subprocess.run(ffmpeg_command)
# output_video = r"E:\ha\hindi_f.mp4"
# input_audio = "hindi.mp3"
# ffmpeg_command = [
#         "ffmpeg",
#         "-y",  # Add the -y flag here to force overwrite
#         "-i",
#         input_video,
#         "-i",
#         input_audio,
#         "-c:v", "copy",
#         # "-vf", r"subtitles='E:\GITHUB Repo\VoiceCraftAI\hindi.srt',scale=1280:720",
#         "-af", "atempo=1.1",
#     "-c:v", "libx264",
#     "-c:a", "aac",
#     "-strict", "experimental",
#     "-map", "0:v",  # Map the video stream from input_video
#     "-map", "1:a",
#         output_video,
#     ]
# subprocess.run(ffmpeg_command)
# output_video = r"E:\ha\kannada_f.mp4"
# input_audio = "kannada.mp3"
# ffmpeg_command = [
#         "ffmpeg",
#         "-y",  # Add the -y flag here to force overwrite
#         "-i",
#         input_video,
#         "-i",
#         input_audio,
#         "-c:v", "copy",
#         # "-vf", r"subtitles='E:\GITHUB Repo\VoiceCraftAI\kannada.srt',scale=1280:720",
#         "-af", "atempo=1.1",
#     "-c:v", "libx264",
#     "-c:a", "aac",
#     "-strict", "experimental",
#     "-map", "0:v",  # Map the video stream from input_video
#     "-map", "1:a",
#         output_video,
#     ]
# subprocess.run(ffmpeg_command)

# convert_file = ConvertFile("shindi.vtt", "utf-8")
# convert_file.convert()

# ffmpeg_command1 = ["ffmpeg", "-i", "hindi_f.mp4", "-vf", "subtitles=shindi.srt::force_style='FontName=Arial,FontSize=13'", "-c:a", "copy", "output_hindi.mp4"]
# subprocess.run(ffmpeg_command1)
# ffmpeg_command2 = ["ffmpeg", "-i", "kannada_f.mp4", "-vf", "subtitles=skannada.srt:force_style='FontName=Arial,FontSize=13'", "-c:a", "copy", "output_kannada_su.mp4"]
# subprocess.run(ffmpeg_command2)
# ffmpeg_command2 = ["ffmpeg", "-i", "tamil_f.mp4", "-vf", "subtitles=stamil.srt:force_style='FontName=Arial,FontSize=13'", "-c:a", "copy", "output_tamil_su.mp4"]
# subprocess.run(ffmpeg_command2)
# ffmpeg_command2 = ["ffmpeg", "-i", "telugu_f.mp4", "-vf", "subtitles=stelugu.srt::force_style='FontName=Arial,FontSize=13'", "-c:a", "copy", "output_telugu.mp4"]
# subprocess.run(ffmpeg_command2)