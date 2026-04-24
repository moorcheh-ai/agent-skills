#!/usr/bin/env python3
"""Upload a file directly to a Moorcheh namespace."""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from moorcheh_conn import get_client

def main():
    parser = argparse.ArgumentParser(description="Upload a file to Moorcheh")
    parser.add_argument("--namespace", required=True, help="Target namespace name")
    parser.add_argument("--file", required=True, help="Path to file (PDF, TXT, MD, CSV, JSON, DOCX)")
    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"❌ File not found: {args.file}")
        sys.exit(1)

    client = get_client()
    try:
        result = client.documents.upload_file(
            namespace_name=args.namespace,
            file_path=args.file
        )
        print(f"✅ Uploaded '{result.get('file_name', args.file)}' to '{args.namespace}'")
        print("⏳ File is being parsed and indexed. Wait before searching.")
    except Exception as e:
        print(f"❌ Error uploading file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
