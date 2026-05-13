#!/usr/bin/env python3
"""List text/summary chunks in a text namespace (Fetch Text Data API)."""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from moorcheh_conn import get_client


def main():
    parser = argparse.ArgumentParser(
        description="Fetch text chunks from a Moorcheh text namespace (max 100 items)"
    )
    parser.add_argument(
        "--namespace",
        required=True,
        help="Text namespace name",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON response",
    )
    args = parser.parse_args()

    client = get_client()
    try:
        data = client.documents.fetch_text_data(namespace_name=args.namespace)
        if args.json:
            print(json.dumps(data, indent=2))
            return

        print(f"Status: {data.get('status')}")
        print(f"Message: {data.get('message')}")
        stats = data.get("statistics")
        if stats:
            print(f"Statistics: {stats}")
        items = data.get("items", [])
        print(f"Items: {len(items)} (max 100 per request)\n")
        for i, item in enumerate(items, 1):
            tid = item.get("id", "?")
            summary = item.get("is_summary")
            text = (item.get("text") or "")[:200]
            print(f"  {i}. id={tid} is_summary={summary}")
            print(f"     {text}...")
            if item.get("metadata"):
                print(f"     metadata: {item['metadata']}")
            print()
        et = data.get("execution_time")
        if et is not None:
            print(f"execution_time: {et}s")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
