#!/usr/bin/env python3
"""Upload a file or directory of files to a Moorcheh namespace."""

import argparse
import glob
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from moorcheh_conn import get_client

def upload_single(client, namespace, file_path):
    result = client.documents.upload_file(
        namespace_name=namespace,
        file_path=file_path
    )
    print(f"[OK] Uploaded '{result.get('file_name', file_path)}' to '{namespace}'")

def main():
    parser = argparse.ArgumentParser(description="Upload a file or directory to Moorcheh")
    parser.add_argument("--namespace", required=True, help="Target namespace name")
    parser.add_argument("--file", help="Path to a single file (PDF, TXT, MD, CSV, JSON, DOCX)")
    parser.add_argument("--dir", help="Path to directory — uploads all supported files")
    args = parser.parse_args()

    if not args.file and not args.dir:
        parser.print_help()
        sys.exit(1)

    client = get_client()

    try:
        if args.file:
            if not os.path.isfile(args.file):
                print(f"[ERROR] File not found: {args.file}")
                sys.exit(1)
            upload_single(client, args.namespace, args.file)
            print("[WAIT] File is being parsed and indexed. Wait before searching.")

        elif args.dir:
            if not os.path.isdir(args.dir):
                print(f"[ERROR] Directory not found: {args.dir}")
                sys.exit(1)
            extensions = ("*.md", "*.txt", "*.pdf", "*.docx", "*.csv", "*.json")
            files = []
            for ext in extensions:
                files.extend(glob.glob(os.path.join(args.dir, ext)))
            if not files:
                print(f"[ERROR] No supported files found in {args.dir}")
                sys.exit(1)
            print(f"Uploading {len(files)} file(s) from '{args.dir}'...")
            for f in sorted(files):
                upload_single(client, args.namespace, f)
            print(f"[OK] Batch upload complete. {len(files)} file(s) uploaded.")
            print("[WAIT] Files are being parsed and indexed. Wait before searching.")

    except Exception as e:
        print(f"[ERROR] Error uploading: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
