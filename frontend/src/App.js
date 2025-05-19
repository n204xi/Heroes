import React, { useState, useEffect } from "react";
import ChatWindow from "./components/ChatWindow";
import MessageInput from "./components/MessageInput";
import CharacterSelect from "./components/CharacterSelect";
import "./App.css";
import "./utils/MobilePolish.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [character, setCharacter] = useState("Sora");
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    if ("Notification" in window && Notification.permission !== "granted") {
      Notification.requestPermission();
    }
  }, []);

  const sendMessage = async (text) => {
    setIsTyping(true);
    const formData = new FormData();
    formData.append("message", text);
    formData.append("character", character);

    const res = await fetch("http://localhost:8000/chat/message", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setMessages((prev) => [
      ...prev,
      { text, from: "user", character },
      { text: data.reply, from: "ai", character, audio: data.audio_url },
    ]);
    setIsTyping(false);
    if (data.audio_url) {
      const audio = new Audio("http://localhost:8000" + data.audio_url);
      audio.play();
    }
    if ("Notification" in window && Notification.permission === "granted") {
      new Notification("Heroes Chatbot", {
        body: data.reply,
        icon: "/icon-512.png", // Place this icon in your public folder if you want a custom icon
      });
    }
  };

  return (
    <div className="app-container">
      <h2>AI Friend Chatbot</h2>
      <CharacterSelect character={character} setCharacter={setCharacter} />
      <ChatWindow messages={messages} />
      {isTyping && <div className="typing-indicator">AI is typing...</div>}
      <MessageInput onSend={sendMessage} />
    </div>
  );
}

export default App;