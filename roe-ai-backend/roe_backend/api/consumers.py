import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps
from channels.db import database_sync_to_async
from .utils import extract_relevant_content

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handle WebSocket connection."""
        self.room_name = "video_chat_room"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Handle received WebSocket messages."""
        text_data_json = json.loads(text_data)
        query = text_data_json.get('query')
        video_url = text_data_json.get('videoUrl')

        if not query or not video_url:
            await self.send(text_data=json.dumps({
                'message': "Query or video URL missing."
            }))
            return

        video_filename = video_url.split('/')[-1]

        try:
            Video = apps.get_model('api.Video')
            video = await database_sync_to_async(self.get_video)(video_filename)

            transcription = video.transcription
            result = extract_relevant_content(transcription, query)
            await self.send(text_data=json.dumps({
                'message': result
            }))

        except Video.DoesNotExist:
            await self.send(text_data=json.dumps({
                'message': "Video not found."
            }))

    def get_video(self, video_filename):
        """Helper method to retrieve the video object synchronously."""
        Video = apps.get_model('api.Video')
        return Video.objects.get(file__icontains=video_filename)