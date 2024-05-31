import os
import subprocess
import shutil
import librosa

def clone_voice(voice_model="vishnu_voice",absolute_path="/home/a/voicecraft/AICoverGen", languages=['kannada']):
    # @title Generate | Output generated inside "AICoverGen\song_output\random_number"
    # @markdown Main Option | You also can input audio path inside "SONG_INPUT"
    
    
    absolute_path = absolute_path
    os.chdir(absolute_path)

    RVC_DIRNAME = voice_model # @param {type:"string"}
    PITCH_CHANGE = 0 # @param {type:"integer"}
    PITCH_CHANGE_ALL = 0 # @param {type:"integer"}
    # @markdown Voice Conversion Options
    INDEX_RATE = 0.5 # @param {type:"number"}
    FILTER_RADIUS = 3 # @param {type:"integer"}
    PITCH_DETECTION_ALGO = "rmvpe" # @param ["rmvpe", "mangio-crepe"]
    CREPE_HOP_LENGTH = 128 # @param {type:"integer"}
    PROTECT = 0.33 # @param {type:"number"}
    REMIX_MIX_RATE = 0.25  # @param {type:"number"}
    # @markdown Audio Mixing Options
    MAIN_VOL = 0 # @param {type:"integer"}
    BACKUP_VOL = 0 # @param {type:"integer"}
    INST_VOL = 0 # @param {type:"integer"}
    # @markdown Reverb Control
    REVERB_SIZE = 0.15 # @param {type:"number"}
    REVERB_WETNESS = 0.2 # @param {type:"number"}
    REVERB_DRYNESS = 0.8 # @param {type:"number"}
    REVERB_DAMPING = 0.7 # @param {type:"number"}
    # @markdown Output Format
    OUTPUT_FORMAT = "mp3" # @param ["mp3", "wav"]

    import subprocess
    lst = languages
    for i in lst:
        #SONG_INPUT = i # @param {type:"string"}
        
        SONG_INPUT = f"/home/a/voicecraft/demo/VoiceCraftAI/audio_files/{i}.mp3"
        command = [
            "python3",
            "src/main.py",
            "-i", SONG_INPUT,
            "-dir", RVC_DIRNAME,
            "-p", str(PITCH_CHANGE),
            "-k",
            "-ir", str(INDEX_RATE),
            "-fr", str(FILTER_RADIUS),
            "-rms", str(REMIX_MIX_RATE),
            "-palgo", PITCH_DETECTION_ALGO,
            "-hop", str(CREPE_HOP_LENGTH),
            "-pro", str(PROTECT),
            "-mv", str(MAIN_VOL),
            "-bv", str(BACKUP_VOL),
            "-iv", str(INST_VOL),
            "-pall", str(PITCH_CHANGE_ALL),
            "-rsize", str(REVERB_SIZE),
            "-rwet", str(REVERB_WETNESS),
            "-rdry", str(REVERB_DRYNESS),
            "-rdamp", str(REVERB_DAMPING),
            "-oformat", OUTPUT_FORMAT
        ]

        # Open a subprocess and capture its output
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        # Print the output in real-time
        for line in process.stdout:
            print(line, end='')

        # Wait for the process to finish
        process.wait()

    savefiles(lst,voice_model)
    

def savefiles(lang=["kannada"],voice_model = "vishnu_voice"):
    for i in lang:
        #saving the outputs to a different folder
        song_path = f"/home/a/voicecraft/AICoverGen/song_output/{i}/{i}_stereo_{voice_model}_p0_i0.5_fr3_rms0.25_pro0.33_rmvpe.wav"
        output_dir = f"/home/a/voicecraft/demo/VoiceCraftAI/output_files/"
        os.makedirs(output_dir,exist_ok = True)
        destination_path = output_dir +f"{i}.wav"
        shutil.copy(song_path,destination_path)
        print(song_path)
        print("File saved into")
        print(destination_path)
        print("Merging the files")
        merge_video(lang = i)

def get_duration(file_path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout:
        duration = float(result.stdout)
        print(duration)
        return duration
    else:
        # Handle case where ffprobe did not return output
        print("Error: Unable to retrieve duration from ffprobe.")
        print(file_path)
        return None

def merge_video(absolute_path="/home/a/voicecraft/demo/VoiceCraftAI",lang = "kannada"):
    absolute_path = absolute_path
    os.chdir(absolute_path)
    audio_directory = 'output_files'
    lang = lang
    input_video = absolute_path + "/demo.mp4"
    input_audio = absolute_path + f"/{audio_directory}/{lang}.wav"
    output_video = absolute_path + f"/video_files/{lang}_f.mp4"
    # subprocess.run([
    #     "ffmpeg", "-i" ,f"{absolute_path}/{audio_directory}/{lang}.wav" ,f"{absolute_path}/{audio_directory}/{lang}.mp3"
    # ])
    #Adjusting the video speed to match the audio
    #video_duration = get_duration(input_video)
    
    #audio_duration = librosa.get_duration(filename=input_audio)

    #speed_factor = audio_duration / video_duration

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

    # #subtitling the video
    # ffmpeg_command1 = ["ffmpeg", "-i", f"video_files/{lang}_f.mp4", "-vf", f"subtitles=srt_files/{lang}.srt:force_style='FontName=Arial,FontSize=13'", "-c:a", "copy", f"final\output_{lang}.mp4"]
    # subprocess.run(ffmpeg_command1)

if __name__ == "__main__":
    clone_voice()
    # i = "hindi"
    # voice_model = "vishnu_voice"
    # song_path = f"/home/vishnu/hackathon/AICoverGen/song_output/{i}/{i}_stereo_{voice_model}_p0_i0.5_fr3_rms0.25_pro0.33_rmvpe.wav"
    # output_dir = f"/home/vishnu/hackathon/demo/VoiceCraftAI/output_files/"
    # os.makedirs(output_dir,exist_ok = True)
    # destination_path = output_dir +f"{i}.wav"
    # shutil.copy(song_path,destination_path)
    # print(song_path)
    # print("File saved into")
    # print(destination_path)