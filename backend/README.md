# AI Friend Chatbot Backend

This document provides an overview of the backend setup for the AI Friend Chatbot project. The backend is built using Python and FastAPI, and it integrates with the OpenAI and ElevenLabs APIs to provide a conversational AI experience.

## Project Structure

The backend is organized as follows:

```
backend/
├── src/
│   ├── app.py                # Main entry point for the FastAPI application
│   ├── routes/               # Contains route definitions
│   │   ├── chat.py           # Handles chat-related routes
│   │   ├── files.py          # Manages file uploads and downloads
│   │   └── notifications.py   # Handles push notifications
│   ├── services/             # Contains service logic for external APIs
│   │   ├── openai_service.py  # Interacts with the OpenAI API
│   │   ├── elevenlabs_service.py # Integrates with ElevenLabs Text-to-Speech API
│   │   └── file_analysis.py   # Analyzes uploaded files using AI tools
│   └── utils/                # Utility functions
│       └── helpers.py        # Assists with various tasks
├── requirements.txt          # Python dependencies for the backend
└── README.md                 # Documentation for the backend
```

## Setup Instructions

1. **Clone the Repository**
   ```
   git clone <repository-url>
   cd ai-friend-chatbot/backend
   ```

2. **Create a Virtual Environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```
   python src/app.py
   ```

## API Usage

The backend exposes several endpoints for interacting with the chatbot:

- **Chat Endpoint**: Send messages to the AI and receive responses.
- **File Upload Endpoint**: Upload documents and images for the AI to analyze.
- **Notification Endpoint**: Receive proactive messages from the AI.

Refer to the individual route files for detailed API specifications.

## Additional Notes

- Ensure you have the necessary API keys for OpenAI and ElevenLabs configured in your environment.
- The backend is designed to work seamlessly with the frontend application, which can be found in the `frontend` directory.

For further assistance, please refer to the documentation in the `frontend` and `database` directories.

# TODOs

- Update this README to reference FastAPI, not Flask
- Ensure requirements.txt is only in backend/, not duplicated in src/
- Expand test coverage in backend/tests/
- Add .env to .gitignore if not present
- Apply error handling and validation patterns from chat.py to all backend route files