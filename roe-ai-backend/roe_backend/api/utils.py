from openai import OpenAI
from moviepy.editor import VideoFileClip
from .models import Video

def transcribe_video(video_id):
    client = OpenAI(api_key="YOUR_OPENAI_API_KEY")
    video = Video.objects.get(id=video_id)
    video_file_path = video.file.path

    clip = VideoFileClip(video_file_path)
    clip.audio.write_audiofile("../media/temp.mp3")

    with open("temp.mp3", "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="vtt"
        )
        print(transcription)
        video.transcription = transcription
        video.transcription_status = 'completed'
        video.save()