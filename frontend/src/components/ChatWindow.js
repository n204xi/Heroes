import React, { useEffect, useRef, useState } from 'react';
import MessageInput from './MessageInput';
import Notification from "./Notification";
import FileUpload from './FileUpload';
import ProfilePicUpload from "./ProfilePicUpload";
import { fetchMessages, sendMessage, saveMessage, fetchProfilePic } from '../utils/api';

const ChatWindow = () => {
    const [messages, setMessages] = useState([]);
    const [notifications, setNotifications] = useState([]);
    const [profilePic, setProfilePic] = useState(null);
    const endRef = useRef(null);

    useEffect(() => {
        const loadMessages = async () => {
            const initialMessages = await fetchMessages();
            setMessages(initialMessages);
        };

        loadMessages();
    }, []);

    useEffect(() => {
        endRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    useEffect(() => {
        if (notifications.length > 0) {
            const timer = setTimeout(() => {
                setNotifications((prev) => prev.slice(1));
            }, 3000); // 3 seconds
            return () => clearTimeout(timer);
        }
    }, [notifications]);

    const handleSendMessage = async (text) => {
        const newMessage = { text, from: 'user' };
        setMessages((prevMessages) => [...prevMessages, newMessage]);
        await saveMessage(newMessage);

        const response = await sendMessage(text);
        setMessages((prevMessages) => [...prevMessages, response]);
        await saveMessage(response);
    };

    const handleNewNotification = (notification) => {
        setNotifications((prevNotifications) => [...prevNotifications, notification]);
    };

    const handleFileUpload = async (file) => {
        const formData = new FormData();
        formData.append("file", file);

        const res = await fetch("http://localhost:8000/chat/upload", {
            method: "POST",
            body: formData,
        });
        const data = await res.json();
        setMessages((prev) => [
            ...prev,
            {
                text: `[File uploaded: ${file.name}]`,
                from: "user",
                fileUrl: data.fileUrl ? "http://localhost:8000" + data.fileUrl : undefined,
                fileType: data.fileType,
                fileName: data.fileName
            },
            {
                text: data.reply,
                from: "ai",
                character: data.character,
                audio: data.audio_url
            }
        ]);
        if (data.audio_url) {
            const audio = new Audio("http://localhost:8000" + data.audio_url);
            audio.play();
        }
    };

    // Poll for new messages every 5 seconds
    useEffect(() => {
        const poll = setInterval(async () => {
            const latest = await fetchMessages();
            if (latest.length > messages.length) {
                const newMsgs = latest.slice(messages.length);
                newMsgs.forEach(msg => {
                    if (msg.from === "ai" && msg.notification) {
                        setNotifications(n => [...n, msg.text]);
                    }
                });
                setMessages(latest);
            }
        }, 5000);
        return () => clearInterval(poll);
    }, [messages]);

    useEffect(() => {
        const loadProfilePic = async () => {
            const res = await fetchProfilePic(character); // character should be in your state/props
            setProfilePic(res.profile_pic_url);
        };
        loadProfilePic();
    }, [character]);

    return (
        <div className="chat-window">
            {/* Profile Pic and Upload */}
            <div style={{ display: "flex", alignItems: "center", marginBottom: 10 }}>
                {profilePic && (
                    <img
                        src={`http://localhost:8000${profilePic}`}
                        alt="Profile"
                        style={{ width: 48, height: 48, borderRadius: "50%", marginRight: 10, objectFit: "cover" }}
                    />
                )}
                <ProfilePicUpload character={character} onUpload={setProfilePic} />
            </div>
            <div className="notifications">
                {notifications.map((msg, idx) => (
                    <Notification
                        key={idx}
                        message={msg}
                        onClose={() => setNotifications(n => n.filter((_, i) => i !== idx))}
                    />
                ))}
            </div>
            <div className="messages" style={{
                height: 400,
                overflowY: "scroll",
                border: "1px solid #ccc",
                marginBottom: 10,
                background: "#f9f9f9",
                padding: 10,
                borderRadius: 8
            }}>
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`message ${msg.from}`}
                        style={{
                            textAlign: msg.from === "user" ? "right" : "left",
                            margin: "8px 0",
                            color: msg.from === "user" ? "#1976d2" : "#333"
                        }}
                    >
                        <b>{msg.character}:</b> {msg.text}
                        {/* Image preview */}
                        {msg.fileType && msg.fileType.startsWith("image/") && msg.fileUrl && (
                            <img src={msg.fileUrl} alt={msg.fileName || "uploaded"} style={{ maxWidth: "80%", marginTop: 8, borderRadius: 8 }} />
                        )}
                        {/* Document link */}
                        {msg.fileType && !msg.fileType.startsWith("image/") && msg.fileUrl && (
                            <a href={msg.fileUrl} target="_blank" rel="noopener noreferrer" style={{ display: "block", marginTop: 8 }}>
                                View Document
                            </a>
                        )}
                        {msg.audio && (
                            <audio controls src={msg.audio.startsWith("http") ? msg.audio : "http://localhost:8000" + msg.audio} style={{ display: "block", margin: "4px 0" }} />
                        )}
                    </div>
                ))}
                <div ref={endRef} />
            </div>
            <FileUpload onFileUpload={handleFileUpload} />
            <MessageInput onSendMessage={handleSendMessage} />
        </div>
    );
};

export default ChatWindow;