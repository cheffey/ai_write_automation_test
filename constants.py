from pathlib import Path
from utils.llm_client import LLMClient

ROOT = Path(__file__).parent
llm_client = LLMClient(
    base_url="http://10.21.76.144:1025/v1",
    api_key="YOUR_API_KEY"
)