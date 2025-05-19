def format_message(user_id, message):
    return {
        "user_id": user_id,
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }

def handle_error(error):
    return {
        "success": False,
        "error": str(error)
    }

def validate_file(file):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'docx'}
    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
        return True
    return False

def save_file(file, upload_folder):
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)
    return file_path

def generate_response_message(ai_response):
    return {
        "success": True,
        "response": ai_response
    }