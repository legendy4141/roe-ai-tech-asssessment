from django.shortcuts import render
import os
import hashlib
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser
from rest_framework.decorators import api_view, parser_classes
from openai import OpenAI
from moviepy.editor import VideoFileClip
from .utils import transcribe_video, find_timestamp_for_query
from .models import Video

def get_file_hash(file):
    hash_md5 = hashlib.md5()
    for chunk in file.chunks():
        hash_md5.update(chunk)
    return hash_md5.hexdigest()

@csrf_exempt
@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload_video(request):
    video = request.FILES.get('video')
    if not video:
        return JsonResponse({'error': 'No video uploaded'}, status=400)

    allowed_types = ['video/mp4', 'video/webm']
    if video.content_type not in allowed_types:
        return JsonResponse({'error': 'Unsupported file type. Only MP4 and WebM are allowed.'}, status=400)

    file_hash = get_file_hash(video)
    existing_video = Video.objects.filter(file_hash=file_hash).first()
    if existing_video:
        file_name = os.path.basename(existing_video.file.name)
        video_url = f"http://127.0.0.1:8000{settings.MEDIA_URL}{file_name}"
        return JsonResponse({'videoUrl': video_url, 'message': 'Video already uploaded'})
        
    save_path = os.path.join(settings.MEDIA_ROOT, video.name)
    with open(save_path, 'wb+') as destination:
        for chunk in video.chunks():
            destination.write(chunk)
    
    clip = VideoFileClip(save_path)
    if clip.duration > 180:
        minutes = int(clip.duration // 60)
        seconds = int(clip.duration % 60)
        return JsonResponse({'error': f"Video length is limited to 3 minutes. Current video length is {minutes} minutes {seconds} seconds."}, status=400)
    
    if not os.path.exists(save_path):
        return JsonResponse({'error': 'File upload failed'}, status=500)
    
    video_url = f"http://127.0.0.1:8000{settings.MEDIA_URL}{video.name}"

    video_obj = Video.objects.create(file=save_path, file_hash=file_hash)
    transcribe_video(video_obj.id)

    return JsonResponse({'videoUrl': video_url})

@api_view(['POST'])
def search_video(request):
    query = request.data.get('query')
    video_url = request.data.get('video_url')

    if not query:
        return JsonResponse({'error': 'No query provided'}, status=400)

    if not video_url:
        return JsonResponse({'error': 'No video URL provided'}, status=400)
    
    video_filename = video_url.split('/')[-1]
    print(video_filename)
    try:
        video = Video.objects.get(file__icontains=video_filename)
        if video.transcription:   
            timestamp_in_seconds = find_timestamp_for_query(video.transcription, query)
            if timestamp_in_seconds == -1:
                return JsonResponse({'error': 'Invalid timestamp format in response'}, status=400)
            return JsonResponse({'timestamp': timestamp_in_seconds}, status=200)
        else:
            return JsonResponse({'error': 'Video not found'}, status=404)
    except Video.DoesNotExist:
        return JsonResponse({'error': 'Video not found'}, status=404)