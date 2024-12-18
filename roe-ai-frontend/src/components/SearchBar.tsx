import { useState } from "react";
import axios from "axios";

interface SearchBarProps {
  onSearchResult: (result: { timestamp: number; description: string }) => void;
  videoUrl: string;
}

const SearchBar: React.FC<SearchBarProps> = ({ onSearchResult, videoUrl }) => {
  const [query, setQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return alert("Please enter a question.");
    setIsSearching(true);

    try {
      const response = await axios.post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/search/`, {
        query,
        video_url: videoUrl,
      });
      console.log(response)
      onSearchResult(response.data);
    } catch (error) {
      if (axios.isAxiosError(error) && error.response) {
        const errorMessage = error.response.data.error || "Search failed!";
        alert(`Search failed: ${errorMessage}`);
      } else {
        console.error("Search failed:", error);
        alert("Search failed!");
      }
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="flex items-center space-x-4 bg-gray-200 rounded-md p-4 shadow">
      <input
        type="text"
        placeholder="Ask a question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="flex-1 px-4 py-2 rounded-md border border-gray-300 focus:outline-none focus:ring focus:ring-blue-400"
      />
      <button
        onClick={handleSearch}
        disabled={isSearching}
        className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:bg-gray-300"
      >
        {isSearching ? "Searching..." : "Search"}
      </button>
    </div>
  );
};

export default SearchBar;