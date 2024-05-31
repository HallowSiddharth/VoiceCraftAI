from moviepy.editor import VideoFileClip
import os

def trim_video(video_path, start_time, end_time):
    # Load the video file
    video = VideoFileClip(video_path)
    
    # Trim the video
    trimmed_video = video.subclip(start_time, end_time)
    
    # Create a temporary file to save the trimmed video
    temp_path = video_path + ".temp.mp4"
    trimmed_video.write_videofile(temp_path, codec="libx264", audio_codec="aac")
    
    # Replace the original video with the trimmed video
    os.remove(video_path)
    os.rename(temp_path, video_path)
    
    # Close the video clips to release resources
    video.close()
    trimmed_video.close()

if __name__ == "__main__":
    # Example usage
    video_path = "/home/a/voicecraft/demo/VoiceCraftAI/demo copy.mp4"
    start_time = 0  # start time in seconds
    end_time = 10    # end time in seconds
    
    trim_video(video_path, start_time, end_time)
    print("Video trimmed successfully.")
