#!/usr/bin/env python3
"""Retrieve indexed text documents by ID from a Moorcheh namespace."""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from moorcheh_conn import get_client


def main():
    parser = argparse.ArgumentParser(
        description="Get documents by ID (max 100 ids per request)"
    )
    parser.add_argument("--namespace", required=True, help="Namespace name")
    parser.add_argument(
        "--ids",
        required=True,
        help='Comma-separated document IDs (e.g. "doc1,doc2")',
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print raw JSON response",
    )
    args = parser.parse_args()

    raw_ids = [x.strip() for x in args.ids.split(",") if x.strip()]
    if not raw_ids:
        print("[ERROR] No ids after parsing --ids")
        sys.exit(1)
    if len(raw_ids) > 100:
        print("[ERROR] Maximum 100 ids per request")
        sys.exit(1)

    client = get_client()
    try:
        data = client.documents.get(
            namespace_name=args.namespace,
            ids=raw_ids,
        )
        if args.json:
            print(json.dumps(data, indent=2))
            return

        print(f"Status: {data.get('status')}")
        print(f"Message: {data.get('message')}")
        print(f"Requested: {data.get('requested_ids')}  Found: {data.get('found_items')}")
        nf = data.get("not_found_ids")
        if nf:
            print(f"Not found: {nf}")
        for item in data.get("items", []):
            print(f"\n--- {item.get('id')} ---")
            text = item.get("text") or ""
            print(text[:500] + ("..." if len(text) > 500 else ""))
            if item.get("metadata"):
                print(f"metadata: {item['metadata']}")
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
