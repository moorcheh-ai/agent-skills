#!/usr/bin/env python3
"""Moorcheh connection helper. Provides a shared client for all scripts."""

import os
import sys

def get_client():
    """Create and return a MoorchehClient instance."""
    try:
        from moorcheh_sdk import MoorchehClient
    except ImportError:
        print("Error: moorcheh-sdk not installed.")
        print("Install with: pip install moorcheh-sdk")
        sys.exit(1)

    api_key = os.environ.get("MOORCHEH_API_KEY")
    if not api_key:
        print("Error: MOORCHEH_API_KEY environment variable not set.")
        print("Get your API key from https://console.moorcheh.ai")
        print("Then run: export MOORCHEH_API_KEY='your-api-key-here'")
        sys.exit(1)

    base_url = os.environ.get("MOORCHEH_BASE_URL", "https://api.moorcheh.ai/v1")
    return MoorchehClient(api_key=api_key, base_url=base_url)


def get_api_headers():
    """Return headers for direct REST API calls."""
    api_key = os.environ.get("MOORCHEH_API_KEY")
    if not api_key:
        print("Error: MOORCHEH_API_KEY environment variable not set.")
        sys.exit(1)
    return {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }


def get_base_url():
    """Return the Moorcheh API base URL."""
    return os.environ.get("MOORCHEH_BASE_URL", "https://api.moorcheh.ai/v1")
