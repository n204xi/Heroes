# AI Friend Chatbot

This project is an AI-powered chatbot that utilizes OpenAI's GPT-4 for conversation and ElevenLabs for voice responses. The chatbot can send and receive messages like a real texting app, share documents and images, and proactively message the user.

## Project Structure

```
ai-friend-chatbot
├── backend
│   ├── src
│   │   ├── app.py
│   │   ├── routes
│   │   │   ├── chat.py
│   │   │   ├── files.py
│   │   │   └── notifications.py
│   │   ├── services
│   │   │   ├── openai_service.py
│   │   │   ├── elevenlabs_service.py
│   │   │   └── file_analysis.py
│   │   └── utils
│   │       └── helpers.py
│   ├── requirements.txt
│   └── README.md
├── frontend
│   ├── src
│   │   ├── App.js
│   │   ├── components
│   │   │   ├── ChatWindow.js
│   │   │   ├── MessageInput.js
│   │   │   ├── FileUpload.js
│   │   │   └── Notification.js
│   │   └── utils
│   │       └── api.js
│   ├── package.json
│   └── README.md
├── database
│   ├── schema.sql
│   └── README.md
└── README.md
```

## Backend

The backend is built using Python and Flask. It handles API requests, processes messages, manages file uploads, and integrates with external services.

### Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd ai-friend-chatbot/backend
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   python src/app.py
   ```

## Frontend

The frontend is built using React. It provides a user interface for chatting with the AI, uploading files, and receiving notifications.

### Setup Instructions

1. **Navigate to the frontend directory:**
   ```
   cd ai-friend-chatbot/frontend
   ```

2. **Install dependencies:**
   ```
   npm install
   ```

3. **Run the application:**
   ```
   npm start
   ```

## Database

The database schema is defined in `schema.sql`. Make sure to set up your database according to the schema provided.

### Setup Instructions

1. **Create the database:**
   ```
   CREATE DATABASE ai_friend_chatbot;
   ```

2. **Run the schema:**
   ```
   source schema.sql
   ```

## Features

- **Chat Interface:** Users can send and receive messages in real-time.
- **File Sharing:** Users can upload documents and images for the AI to analyze.
- **Voice Responses:** The AI responds using ElevenLabs Text-to-Speech.
- **Proactive Messaging:** The AI can initiate conversations based on user activity.

## Contributing

Feel free to submit issues or pull requests to improve the project. 

## License

This project is licensed under the MIT License.

# Updated: This project uses FastAPI (not Flask) and MongoDB (not SQL).
#
# TODOs for workspace consistency and best practices:
# - Remove duplicate requirements.txt in backend/src/ if present; use only backend/requirements.txt
# - Expand backend/tests/test_app.py to cover all routes and error cases
# - Apply error handling and validation patterns from chat.py to all backend route files
# - Clean up unused dependencies in requirements.txt and frontend/package.json
# - Add .env to .gitignore if not already present
# - Remove or update database/schema.sql to clarify MongoDB is used
# - Update database/README.md to clarify MongoDB is used, not SQL
# - Add root-level README.md with project structure and setup instructions
# - Ensure frontend/src/utils/api.js handles API errors gracefully
# - Remove unused files and code in frontend/src/components/
# - Use environment variables for API URLs and secrets in frontend
# - Regularly audit .gitignore and secrets handling