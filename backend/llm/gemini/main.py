import google.generativeai as genai
from pathlib import Path
from typing import Optional, Dict, Any
import os
import json
from dotenv import load_dotenv
import argparse
from style_config import STYLE_CONFIGS

def load_credentials():
    """
    Load credentials from multiple possible sources
    Returns:
        tuple: (api_key, model_name)
    """
    # First try GitHub Actions environment variables
    api_key = os.environ.get('GEMINI_API_KEY')
    model_name = os.environ.get('GEMINI_MODEL_NAME')
    
    # If not found in environment, try loading from .env file
    if not api_key:
        # Try different possible paths for .env file
        possible_paths = [
            Path(__file__).resolve().parent / ".env",  # Same directory as script
            Path(__file__).resolve().parent.parent.parent / ".env",  # Project root
            Path.cwd() / ".env"  # Current working directory
        ]
        
        for env_path in possible_paths:
            if env_path.exists():
                load_dotenv(env_path)
                api_key = os.getenv('GEMINI_API_KEY')
                model_name = os.getenv('GEMINI_MODEL_NAME')
                if api_key:
                    break
    
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY not found in environment variables or .env file. "
            "Please set it in GitHub secrets or provide a .env file."
        )
    
    # Use default model if none specified
    if not model_name:
        model_name = 'gemini-pro'
    
    return api_key, model_name

def load_knowledge_data(file_path: Optional[str] = None, raw_json: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Load knowledge data from either a file or raw JSON string
    """
    try:
        if raw_json:
            return json.loads(raw_json)
        elif file_path:
            with open(file_path, 'r') as f:
                return json.load(f)
        return None
    except json.JSONDecodeError as e:
        print(f"Warning: Invalid JSON format: {e}")
        return None
    except Exception as e:
        print(f"Warning: Could not load knowledge data: {e}")
        return None

def process_knowledge_json(json_data: Dict[str, Any]) -> str:
    """Process JSON knowledge data into a formatted context string"""
    try:
        context = "Based on the following saved content:\n\n"
        
        if isinstance(json_data, dict):
            if "saved" in json_data:  # Reddit-style saved posts
                for item in json_data["saved"]:
                    context += f"Title: {item.get('title', 'Untitled')}\n"
                    context += f"Created: {item.get('created_utc', 'Unknown date')}\n"
                    context += f"Content: {item.get('text', '').strip()}\n\n"
                    if "comments" in item:
                        for comment in item["comments"]:
                            context += f"Comment: {comment.get('text', '').strip()}\n\n"
            else:  # Single item
                context += f"Content: {json.dumps(json_data, indent=2)}\n\n"
        
        return context.strip()
    except Exception as e:
        print(f"Warning: Error processing knowledge JSON: {e}")
        return str(json_data)  # Fallback to raw string representation

def get_chat_response(
    user_input: str,
    style: str = "normal",
    custom_system_prompt: Optional[str] = None,
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    knowledge_json: Optional[Dict[str, Any]] = None
) -> str:
    """Get response from Gemini with specified style configuration"""
    try:
        # Validate style
        style = style.lower()
        if style not in STYLE_CONFIGS:
            raise ValueError(f"Invalid style. Choose from: {', '.join(STYLE_CONFIGS.keys())}")
        
        # Get credentials if not provided
        if not api_key:
            api_key, default_model = load_credentials()
            model_name = model_name or default_model
            
        # Configure Gemini with the API key
        genai.configure(api_key=api_key)
        
        # Initialize the model
        model = genai.GenerativeModel(model_name)
        
        # Prepare the chat
        chat = model.start_chat(history=[])
        
        # Use custom system prompt if provided, otherwise use style's default
        system_prompt = custom_system_prompt or STYLE_CONFIGS[style]["system_prompt"]
        
        # If knowledge JSON is provided, process it and add to system prompt
        if knowledge_json:
            context = process_knowledge_json(knowledge_json)
            system_prompt = f"{system_prompt}\n\nContext for your response:\n{context}"
        
        # Send system prompt
        chat.send_message(system_prompt)
        
        # Get response with style-specific configuration
        response = chat.send_message(
            user_input,
            generation_config=STYLE_CONFIGS[style]["generation_config"]
        )
        
        if not response.text:
            return "No response generated. Please try again."
        
        return response.text

    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description='Get AI response using Gemini')
    parser.add_argument('--input', '-i', type=str, required=True, 
                      help='User input text')
    parser.add_argument('--style', '-s', type=str,
                      choices=list(STYLE_CONFIGS.keys()),
                      default='normal',
                      help='Response style')
    parser.add_argument('--system-prompt', '-p', type=str,
                      help='Optional custom system prompt to override style default')
    parser.add_argument('--model', '-m', type=str,
                      help='Model name (default: gemini-pro)')
    parser.add_argument('--api-key', '-k', type=str,
                      help='Gemini API key (optional, can be set in env or .env file)')
    parser.add_argument('--knowledge-file', '-jf', type=str,
                      help='Path to JSON file containing knowledge data')
    parser.add_argument('--knowledge-raw', '-jr', type=str,
                      help='Raw JSON string containing knowledge data')
    parser.add_argument('--debug', '-d', action='store_true',
                      help='Enable debug output')
    
    args = parser.parse_args()
    
    # Load knowledge data from either file or raw JSON
    knowledge_json = None
    if args.knowledge_file or args.knowledge_raw:
        knowledge_json = load_knowledge_data(
            file_path=args.knowledge_file,
            raw_json=args.knowledge_raw
        )
        if args.debug and knowledge_json:
            print(f"\nDebug - Loaded knowledge data:\n{json.dumps(knowledge_json, indent=2)}\n")
    
    # Get response
    response = get_chat_response(
        user_input=args.input,
        style=args.style,
        custom_system_prompt=args.system_prompt,
        model_name=args.model,
        api_key=args.api_key,
        knowledge_json=knowledge_json
    )
    
    if response:
        print(response)
    else:
        print("Error: No response generated")

if __name__ == "__main__":
    main()