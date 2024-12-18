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

def convert_to_seconds(timestamp: str) -> float:
    try:
        parts = timestamp.split(":")
        if len(parts) != 3:
            raise ValueError("Timestamp must be in hh:mm:ss.ms format")

        seconds_and_ms = parts[2].split(".")
        if len(seconds_and_ms) != 2:
            raise ValueError("Timestamp seconds part must include milliseconds (hh:mm:ss.ms)")

        hours, minutes = int(parts[0]), int(parts[1])
        seconds = int(seconds_and_ms[0])
        milliseconds = int(seconds_and_ms[1])
        
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
        return total_seconds

    except ValueError as e:
        print(f"Error: {e}")
        return None

def find_timestamp_for_query(transcript, query):
    client = OpenAI(api_key="YOUR_OPENAI_API_KEY")
    completion = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": """
                    You are a helpful video analyzer. When provided with a transcription and a query, your task is to find the **start timestamp** of the sentence where the query is mentioned in the transcription. 
                    Your response should be in the format `hh:mm:ss:ms` (e.g., 00:01:23.450), including milliseconds if available. 
                    If the query is not found, respond with `Query not found`.
                    Do not include any extra text, just the start timestamp or 'Query not found'.
                """
            },
            {
                "role": "user",
                "content": f"Transcription: {transcript}, Query: {query}"
            }
        ]
    )
    result = completion.choices[0].message.content
    print(result)
    if result.strip().lower() == 'query not found':
        return -1

    timestamp_in_seconds = convert_to_seconds(result.strip())
    return timestamp_in_seconds