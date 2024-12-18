# Roe AI Tech Assessment

This project provides a web application that allows users to upload a video, search within it, and interact with chatbot via a real-time chat feature. It uses Django, Django Channels for WebSockets, and React for the frontend.

## Features
- Video Upload: Users can upload a video file to the server.
- Video Playback: A video player is available for users to play the uploaded video.
- Search within Video: Users can search for specific text within the video and get the timestamp for that query.
- Real-time Chat: A live chat feature is integrated, allowing users to communicate with a chatbot in real-time while watching the video.

## Approach & Architectural Decisions

### 1. **Django Framework**:
   - The backend is built using Django to manage the overall application logic and serve as the primary framework for RESTful APIs and database management.
   - Django's `models.py` is used to define the `Video` model, which stores information about the uploaded video files and their transcriptions.

### 2. **Channels & WebSockets**:
   - Django Channels is utilized for real-time communication via WebSockets. This allows users to chat while watching videos in sync with timestamps.
   - WebSockets are handled through a `ChatConsumer` in `consumers.py`, which allows users to connect to a video chat room and search for specific timestamps within video transcriptions.

### 3. **Video Upload & Transcription Search**:
   - Videos are uploaded via the `VideoUpload` component and stored in a media directory defined in the Django settings.
   - Each video has an associated transcription, which can be searched through via a WebSocket connection by sending a query. The system returns the timestamp corresponding to the query.

### 4. **Database Management**:
   - A SQLite database is used to store video metadata and transcription data. The `Video` model includes fields for the video file, transcription text, and a unique hash for each video to prevent duplicates.
   
### 5. **Video Playback & Seeking**:
   - The frontend (React) utilizes a `VideoPlayer` component to display the video and automatically seek to the timestamp when a query is matched.

## Trade-offs & Considerations

### 1. **Database Choice (SQLite)**:
   - Initially, SQLite is used for simplicity and ease of development. This choice simplifies database setup and migrations but may not scale well for large amounts of video data or high-concurrency use cases. In production, switching to a more scalable database like PostgreSQL or MySQL might be necessary.

### 2. **In-memory Channel Layer**:
   - For simplicity, the channel layer uses an in-memory backend by default. This decision eliminates the need for Redis in development but may cause issues with scaling across multiple instances. In a production environment, Redis should be configured to manage WebSocket connections efficiently.

### 3. **Real-Time Performance**:
   - Real-time interactions are handled with WebSockets, which are suitable for low-latency communication. However, the application may experience performance limitations when handling multiple WebSocket connections simultaneously, especially without Redis or another message broker in place.

### 4. **Media Handling**:
   - Video files are stored in a `media/` directory, and media URLs are served by Django during development. For production environments, additional considerations for video storage and delivery (e.g., using AWS S3, or a dedicated video streaming service) will be required.

## Future Improvements

### 1. **Celery Integration**:
   - Integrate Celery to handle asynchronous tasks, such as transcription processing or video file conversion.
### 2. **Caching**:
   - Implement caching for frequently searched video transcriptions to improve performance.
### 3. **Advanced Search Features**:
   - Enhance the transcription search functionality by allowing fuzzy search or leveraging machine learning models to improve search accuracy.
### 4. **Scalability**:
   - To handle more users and larger video files, integrate a more scalable database and storage solution (e.g., AWS RDS, PostgreSQL, AWS S3).