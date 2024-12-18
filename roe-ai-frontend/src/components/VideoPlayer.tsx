import { useEffect, useRef, useState } from "react";

interface VideoPlayerProps {
  videoUrl: string;
  seekToTimestamp?: number;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ videoUrl, seekToTimestamp }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [isPlaying, setIsPlaying] = useState(false);

  return (
    <div className="relative w-full h-[580px] bg-gray-300 rounded-md overflow-hidden">
      {/* If videoUrl exists, render the video */}
      {videoUrl ? (
        <video
          ref={videoRef}
          src={videoUrl}
          controls
          className="w-full h-full object-cover bg-black"
        />
      ) : (
        /* Placeholder content with fixed height */
        <div className="flex items-center justify-center w-full h-full text-gray-600">
          <p>No video uploaded</p>
        </div>
      )}
    </div>
  );
};

export default VideoPlayer;