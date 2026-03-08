# Project Setup Contract

All Moorcheh cookbook applications must follow this shared setup contract.

## Python Project Structure

```
project/
├── .env                # Environment variables (never commit)
├── requirements.txt    # Python dependencies
├── main.py             # Application entry point
├── src/
│   ├── __init__.py
│   ├── client.py       # Moorcheh client initialization
│   ├── config.py       # Configuration management
│   └── ...             # Application-specific modules
└── README.md
```

## Requirements File

```
moorcheh-sdk>=0.1.0
python-dotenv>=1.0.0
```

## Client Initialization Pattern

```python
# src/client.py
import os
from moorcheh_sdk import MoorchehClient

def get_client() -> MoorchehClient:
    """Create Moorcheh client from environment variables."""
    api_key = os.environ.get("MOORCHEH_API_KEY")
    if not api_key:
        raise ValueError(
            "MOORCHEH_API_KEY not set. "
            "Get your key from https://console.moorcheh.ai"
        )
    return MoorchehClient(api_key=api_key)
```

## Configuration Pattern

```python
# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

MOORCHEH_API_KEY = os.environ.get("MOORCHEH_API_KEY")
MOORCHEH_BASE_URL = os.environ.get("MOORCHEH_BASE_URL", "https://api.moorcheh.ai/v1")
NAMESPACE = os.environ.get("MOORCHEH_NAMESPACE", "default")
```

## Environment File Template

```env
# .env
MOORCHEH_API_KEY=your-api-key-here
MOORCHEH_NAMESPACE=my-namespace
```

## Common Dependencies

| Package | Purpose |
|---|---|
| `moorcheh-sdk` | Official Moorcheh Python SDK |
| `python-dotenv` | Load environment variables from .env |
| `fastapi` | Web API framework (for API-based apps) |
| `uvicorn` | ASGI server for FastAPI |
| `langchain-moorcheh` | LangChain integration (if using LangChain) |
