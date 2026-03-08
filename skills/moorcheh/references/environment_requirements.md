# Environment Requirements

## Required Environment Variables

| Variable | Required | Description |
|---|---|---|
| `MOORCHEH_API_KEY` | **Yes** | Your Moorcheh API key from [console.moorcheh.ai](https://console.moorcheh.ai) |
| `MOORCHEH_BASE_URL` | No | API base URL (default: `https://api.moorcheh.ai/v1`) |

## Setting Environment Variables

```bash
# Linux / macOS
export MOORCHEH_API_KEY="your-api-key-here"

# Windows PowerShell
$env:MOORCHEH_API_KEY = "your-api-key-here"

# Windows CMD
set MOORCHEH_API_KEY=your-api-key-here
```

## Getting Your API Key

1. Sign up at [console.moorcheh.ai](https://console.moorcheh.ai)
2. Navigate to API Keys section
3. Generate a new API key
4. Store it securely — never commit to version control

## Authentication Header

All API requests use the `x-api-key` header:

```
x-api-key: your-api-key-here
```

## Python SDK Authentication

```python
from moorcheh_sdk import MoorchehClient

# Option 1: Explicit API key
client = MoorchehClient(api_key="your-api-key-here")

# Option 2: From environment variable (recommended)
import os
client = MoorchehClient(api_key=os.environ["MOORCHEH_API_KEY"])

# Option 3: Context manager for automatic cleanup
with MoorchehClient(api_key=os.environ["MOORCHEH_API_KEY"]) as client:
    # Your code here
    pass
```

## Python Dependencies

```bash
pip install moorcheh-sdk requests
```

Or with uv:
```bash
uv pip install moorcheh-sdk requests
```

## Security Best Practices

- Store API keys in environment variables, not in code
- Never commit API keys to version control
- Use secret management services in production
- Rotate keys regularly via the Moorcheh console
- Implement rate limiting with exponential backoff
