from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import os

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

def get_google_doc_text(doc_id):
    creds = None
    token_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../token.json'))
    creds_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../credentials.json'))
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    service = build('docs', 'v1', credentials=creds)
    doc = service.documents().get(documentId=doc_id).execute()
    text = ""
    for element in doc.get("body", {}).get("content", []):
        if "paragraph" in element:
            for run in element["paragraph"].get("elements", []):
                text += run.get("textRun", {}).get("content", "")
    return text