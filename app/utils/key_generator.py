import secrets
import base64

def generate_chat_id():
    # Generate 24 bytes of secure random data
    random_bytes = secrets.token_bytes(24)

    # Encode it with URL-safe base64 and strip padding
    encoded = base64.urlsafe_b64encode(random_bytes).decode("utf-8").rstrip("=")

    return f"chatcmpl-{encoded}"