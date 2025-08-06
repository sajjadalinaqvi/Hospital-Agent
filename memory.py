# memory.py
import json
import os
from datetime import datetime

# ✅ Define the conversation log file path
LOG_FILE = "conversation_log.json"


def load_history():
    """
    Load the full conversation history from the log file.

    Returns:
        list: A list of message dictionaries with role and content.
    """
    if not os.path.exists(LOG_FILE):
        return []

    try:
        with open(LOG_FILE, "r", encoding="utf-8") as file:
            history = json.load(file)
            if isinstance(history, list):
                return history
    except (json.JSONDecodeError, IOError):
        pass

    return []


def update_history(role, content):
    """
    Append a new message to the conversation history.

    Args:
        role (str): 'user' or 'assistant'
        content (str): Message text content
    """
    history = load_history()
    history.append({
        "role": role,
        "content": content,
    })

    try:
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=2)
    except IOError:
        print("⚠️ Could not save conversation history.")


def get_messages():
    return [
        {"role": msg["role"], "content": msg["content"]}
        for msg in load_history()
    ]



def clear_history():
    """
    Clear the entire conversation history by resetting the log file.
    """
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as file:
            json.dump([], file)
    except IOError:
        print("⚠️ Could not clear conversation history.")
