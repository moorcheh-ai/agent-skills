#!/usr/bin/env python3
"""Upload text documents to a Moorcheh namespace."""

import argparse
import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from moorcheh_conn import get_client

def main():
    parser = argparse.ArgumentParser(description="Upload text documents to Moorcheh")
    parser.add_argument("--namespace", required=True, help="Target namespace name")
    parser.add_argument("--file", required=True, help="JSON file with documents array")
    args = parser.parse_args()

    try:
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"❌ File not found: {args.file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in {args.file}: {e}")
        sys.exit(1)

    documents = data if isinstance(data, list) else data.get("documents", [])
    if not documents:
        print("❌ No documents found in file. Expected a JSON array or {\"documents\": [...]}")
        sys.exit(1)

    client = get_client()
    try:
        result = client.documents.upload(
            namespace_name=args.namespace,
            documents=documents
        )
        count = result.get("documents_processed", len(documents))
        print(f"✅ Uploaded {count} document(s) to '{args.namespace}'")
        print("⏳ Documents are being indexed. Wait a few seconds before searching.")
    except Exception as e:
        print(f"❌ Error uploading documents: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
