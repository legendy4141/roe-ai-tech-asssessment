import { useState, useEffect, KeyboardEvent } from "react";
import "../app/styles/ChatBox.css";

const WEBSOCKET_URL = "ws://127.0.0.1:8000/ws/chat/";

const ChatBox: React.FC<{ videoUrl: string }> = ({ videoUrl }) => {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<{ text: string; sender: "user" | "bot" }[]>([]);
  const [ws, setWs] = useState<WebSocket | null>(null);

  useEffect(() => {
    const socket = new WebSocket(WEBSOCKET_URL);

    socket.onopen = () => console.log("WebSocket connected.");
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const botMessage = data.message
      setMessages((prev) => [...prev, { text: botMessage, sender: "bot" }]);
    };

    socket.onclose = () => console.log("WebSocket closed.");
    setWs(socket);

    return () => socket.close();
  }, []);

  const handleSendMessage = () => {
    if (query.trim() && ws?.readyState === WebSocket.OPEN) {
      setMessages((prev) => [...prev, { text: query, sender: "user" }]);
      ws.send(JSON.stringify({ query, videoUrl }));
      setQuery("");
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") handleSendMessage();
  };

  return (
    <div className="chat-container">
      <div className="chat-box">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.sender}`}>
            <div className="message-content">{msg.text}</div>
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          placeholder="Ask something..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
};

export default ChatBox;