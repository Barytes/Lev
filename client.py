import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).with_name(".env"))

# AI Builders Space API configuration
BASE_URL = "https://space.ai-builders.com/backend/v1"

DEFAULT_MODEL = "grok-4-fast"


def get_api_key() -> str:
    """Get API key from environment."""
    api_key = os.getenv("BUILDER_API_KEY")
    if not api_key:
        raise ValueError("BUILDER_API_KEY not configured in environment")
    return api_key


def get_openai_client() -> OpenAI:
    """Get OpenAI client configured for AI Builders Space."""
    return OpenAI(base_url=BASE_URL, api_key=get_api_key())


def get_http_client() -> httpx.Client:
    """Get HTTP client with authorization header for AI Builders Space."""
    return httpx.Client(
        base_url=BASE_URL,
        headers={"Authorization": f"Bearer {get_api_key()}"},
        timeout=30.0,
    )
