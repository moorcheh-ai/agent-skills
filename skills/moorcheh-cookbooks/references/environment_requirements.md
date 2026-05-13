# Environment Requirements (Cookbooks)

See the core skill's [Environment Requirements](../../moorcheh/references/environment_requirements.md) for full details.

## Quick Reference

```bash
# Required
export MOORCHEH_API_KEY="your-api-key-here"

# Optional (app-specific)
export MOORCHEH_NAMESPACE="your-namespace-name"
```

Use **https://api.moorcheh.ai/v1** for Moorcheh REST requests in examples and HTTP clients.

## Additional Dependencies for Cookbooks

```bash
pip install moorcheh-sdk python-dotenv fastapi uvicorn
```
