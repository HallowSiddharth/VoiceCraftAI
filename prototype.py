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
from pytube import YouTube
import subprocess
import sys

# args = sys.argv
# url = args[0]

url = "https://www.youtube.com/watch?v=iIrr5afHnlo"

# Initialize the ASR pipeline
whisper = pipeline("automatic-speech-recognition", model="openai/whisper-medium")

# download the video and convert the audio

directory = r"E:\current file edits new"
video = YouTube(url)
# myvideo = video.streams.get_highest_resolution()
streams = video.streams.filter(res="1080p")
selected_stream = streams.first()
if selected_stream != None:
    myvideo = video.streams.filter(res="1080p")
    audio = video.streams.get_audio_only()
    # downloading and renaming the audio
    name = audio.default_filename
    temp = "temp.mp3"
    audio.download(output_path=directory)
    ffmpegcommand = [
        "ffmpeg",
        "-y",
        "-i",
        directory + "\\" + name,
        directory + "\\" + temp,
    ]
    subprocess.run(ffmpegcommand)
    selected_stream = myvideo.first()
    selected_stream.download(output_path=directory)
    input_video = directory + "\\" + name
    output_video = directory + "\\" + "temp2.mp4"
    input_audio = directory + "\\" + temp
    ffmpeg_command = [
        "ffmpeg",
        "-y",  # Add the -y flag here to force overwrite
        "-i",
        input_video,
        "-i",
        input_audio,
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-strict",
        "experimental",
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-shortest",
        output_video,
    ]
    subprocess.run(ffmpeg_command)

    # cleaning up all the temp files
    os.remove(input_video)

    # renaming our output file to original video name
    os.rename(output_video, input_video)


else:
    myvideo = video.streams.get_highest_resolution()
    myvideo.download(output_path=directory)
    audio = video.streams.get_audio_only()
    name = audio.default_filename
    temp = "temp.mp3"
    audio.download(output_path=directory)
    os.rename(directory + "\\" + name, directory + "\\" + temp)
    input_audio = directory + "\\" + temp


# Define the audio file path
audio_file = input_audio

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
for i, start_time in enumerate(range(0, len(audio), chunk_size_ms)):
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
