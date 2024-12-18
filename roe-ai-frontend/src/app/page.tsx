"use client";

import { useState } from "react";
import VideoUpload from "@/components/VideoUpload";
import SearchBar from "@/components/SearchBar";
import VideoPlayer from "@/components/VideoPlayer";

export default function Home() {
  const [videoUrl, setVideoUrl] = useState<string>("");
  const [searchResult, setSearchResult] = useState<{ timestamp: number; description: string } | null>(null);

  const handleVideoUploaded = (url: string) => setVideoUrl(url);
  const handleSearchResult = (result: { timestamp: number; description: string }) => setSearchResult(result);

  return (
    <div className="container mx-auto p-6">
      <div className="mb-6 text-center">
        <SearchBar videoUrl={videoUrl} onSearchResult={handleSearchResult} />
      </div>

      <div className="flex space-x-8">
        <div className="flex-1 space-y-6">
          <div className="video-container">
            <VideoPlayer videoUrl={videoUrl} seekToTimestamp={searchResult?.timestamp} />
          </div>

          {searchResult && (
            <div className="bg-gray-100 p-4 rounded-md shadow">
              <h3 className="text-xl font-semibold">Search Result:</h3>
              <p>{searchResult.description}</p>
              <p className="text-sm text-gray-500">Timestamp: {searchResult.timestamp} seconds</p>
            </div>
          )}
        </div>

        <div className="space-y-6">
          <VideoUpload onVideoUploaded={handleVideoUploaded} />
        </div>
      </div>
    </div>
  );
}