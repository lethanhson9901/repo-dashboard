import logging
import os
import json
import random
from multiprocessing import Queue, Lock
import google.generativeai as genai
from dotenv import load_dotenv

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO, format='[PID %(process)d] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# --- Environment and API Key Setup ---
load_dotenv()

def load_api_keys() -> list:
    """Load and validate API keys from environment variables."""
    api_keys = json.loads(os.getenv('GOOGLE_API_KEYS_JSON', '[]'))
    if not api_keys:
        raise EnvironmentError("No API keys found in the environment. Please configure them in your .env file.")
    return api_keys

API_KEYS = load_api_keys()
random.shuffle(API_KEYS)  # Randomize for more even distribution

# Queue and Lock for unique API key handling across processes
api_key_queue = Queue()
api_lock = Lock()

# Populate Queue with API keys
for api_key in API_KEYS:
    api_key_queue.put(api_key)

def set_api_key() -> str:
    """Acquire a unique API key and configure the Generative AI client."""
    with api_lock:
        if api_key_queue.empty():
            raise RuntimeError("No API keys available for assignment.")
        api_key = api_key_queue.get()
    genai.configure(api_key=api_key)
    logger.info(f"Using API key: {api_key[:4]}...{api_key[-4:]}")
    return api_key

def release_api_key(api_key: str) -> None:
    """Return the API key to the queue for reuse by other processes."""
    with api_lock:
        api_key_queue.put(api_key)
    logger.info(f"Released API key: {api_key[:4]}...{api_key[-4:]}")