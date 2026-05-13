#!/usr/bin/env python3
"""List raw file objects in document storage for a Moorcheh namespace."""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from moorcheh_conn import get_client


def main():
    parser = argparse.ArgumentParser(
        description="List files in S3-backed storage for a namespace (not indexed chunk listing)"
    )
    parser.add_argument("--namespace", required=True, help="Namespace name")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON response",
    )
    args = parser.parse_args()

    client = get_client()
    try:
        data = client.documents.list_files(namespace_name=args.namespace)
        if args.json:
            print(json.dumps(data, indent=2))
            return

        print(f"Namespace: {data.get('namespace')}")
        print(f"File count: {data.get('file_count', 0)}")
        for f in data.get("files", []):
            fn = f.get("file_name", "?")
            sz = f.get("size", "?")
            lm = f.get("last_modified", "")
            print(f"  - {fn}  ({sz} bytes)  {lm}")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
