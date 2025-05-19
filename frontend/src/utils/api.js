import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000'; // Adjust the base URL as needed

export const sendMessage = async (message) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/chat`, { message });
        return response.data;
    } catch (error) {
        console.error('Error sending message:', error);
        throw error;
    }
};

export const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await axios.post(`${API_BASE_URL}/files/upload`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    } catch (error) {
        console.error('Error uploading file:', error);
        throw error;
    }
};

export const getNotifications = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/notifications`);
        return response.data;
    } catch (error) {
        console.error('Error fetching notifications:', error);
        throw error;
    }
};

export async function fetchMessages() {
  const res = await fetch("http://localhost:8000/chat/history");
  if (!res.ok) return [];
  return await res.json();
}

export async function saveMessage(message) {
  await fetch("http://localhost:8000/chat/history", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(message),
  });
}

export async function uploadProfilePic(character, file) {
  const formData = new FormData();
  formData.append("character", character);
  formData.append("file", file);
  const res = await fetch("http://localhost:8000/profile/upload_profile_pic", {
    method: "POST",
    body: formData,
  });
  return await res.json();
}

export async function fetchProfilePic(character) {
  const res = await fetch(`http://localhost:8000/profile/profile_pic?character=${encodeURIComponent(character)}`);
  return await res.json();
}