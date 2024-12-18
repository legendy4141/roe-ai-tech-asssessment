import { useState } from "react";
import axios from "axios";
import "../app/styles/VideoUpload.css"

interface VideoUploadProps {
  onVideoUploaded: (url: string) => void;
}

const VideoUpload: React.FC<VideoUploadProps> = ({ onVideoUploaded }) => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) {
      setFile(null);
      setErrorMessage(null);
      return;
    }

    const selectedFile = e.target.files[0];
    const allowedTypes = ["video/mp4", "video/webm"];
    if (!allowedTypes.includes(selectedFile.type)) {
      setErrorMessage("Invalid file type. Only MP4 and WebM are supported.");
      setFile(null);
      e.target.value = "";
      return;
    }

    setErrorMessage(null);
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file!");
    setIsUploading(true);

    const formData = new FormData();
    formData.append("video", file);

    try {
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/upload/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 60000,
      });

      console.log("Response from backend:", response.data);
      onVideoUploaded(response.data.videoUrl);
    } catch (error: any) {
      console.error("Upload failed:", error);
      setErrorMessage("Upload failed! Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="video-upload-container flex items-center justify-between space-x-4">

      <input
        type="file"
        accept="video/mp4,video/webm"
        onChange={handleFileChange}
        id="file-input"
        className="hidden"
      />

      <label
        htmlFor="file-input"
        className="cursor-pointer px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
      >
        {file ? "Change File" : "Choose File"}
      </label>

      <span className="text-gray-700 text-sm truncate max-w-xs">
        {file ? file.name : "No file selected"}
      </span>

      <button
        onClick={handleUpload}
        disabled={isUploading || !file}
        className={`px-4 py-2 rounded-md ${
          isUploading || !file
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-green-500 hover:bg-green-600 text-white"
        }`}
      >
        {isUploading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
};

export default VideoUpload;
