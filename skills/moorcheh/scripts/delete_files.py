#!/usr/bin/env python3
"""Delete file objects by name from Moorcheh document storage for a namespace."""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from moorcheh_conn import get_client


def main():
    parser = argparse.ArgumentParser(
        description="Delete files by name from namespace storage (not indexed document IDs)"
    )
    parser.add_argument("--namespace", required=True, help="Namespace name")
    parser.add_argument(
        "--files",
        required=True,
        help='Comma-separated file names (e.g. "a.pdf,b.docx")',
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON response",
    )
    args = parser.parse_args()

    file_names = [n.strip() for n in args.files.split(",") if n.strip()]
    if not file_names:
        print("[ERROR] No file names after parsing --files")
        sys.exit(1)

    client = get_client()
    try:
        data = client.documents.delete_files(
            namespace_name=args.namespace,
            file_names=file_names,
        )
        if args.json:
            print(json.dumps(data, indent=2))
            return

        print(data.get("message", data))
        for row in data.get("results", []):
            print(f"  {row.get('file_name')}: {row.get('status')}- {row.get('message', '')}")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
