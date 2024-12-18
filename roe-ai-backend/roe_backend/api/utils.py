from openai import OpenAI
from moviepy.editor import VideoFileClip

OPENAI_API_KEY = ""

def transcribe_video(video_id):
    """Transcribe the audio from a video file"""
    from .models import Video
    client = OpenAI(api_key=OPENAI_API_KEY)

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
        video.transcription = transcription
        video.transcription_status = 'completed'
        video.save()

def convert_to_seconds(timestamp: str) -> float:
    """Convert a timestamp string to total seconds"""
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
        return None

def find_timestamp_for_query(transcript, query):
    """Find the timestamp of a query in the video transcription"""
    client = OpenAI(api_key=OPENAI_API_KEY)
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

    # Return -1 if the query is not found
    if result.strip().lower() == 'query not found':
        return -1

    # Convert timestamp string to seconds
    timestamp_in_seconds = convert_to_seconds(result.strip())
    return timestamp_in_seconds

def chat_with_user(transcript, query):
    """Engage in a conversation with the user based on the provided transcription and query."""
    client = OpenAI(api_key=OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": """
                    ou are a helpful companion who engages in conversations based on provided transcriptions. 
                    The user will ask questions or share thoughts related to a transcription, and your task is to provide thoughtful, relevant, and engaging responses.
                    Respond in a conversational, friendly, and informative tone. You can reference parts of the transcription where relevant but do not just extract phrases—ensure your answers are part of an ongoing dialogue.
                    Your goal is to make the conversation flow naturally and engage with the user on a deeper level, reflecting on the content in the transcription and asking questions where appropriate.
                """
            },
            {
                "role": "user",
                "content": f"Transcription: {transcript}, Query: {query}"
            }
        ]
    )

    result = completion.choices[0].message.content

    return result
