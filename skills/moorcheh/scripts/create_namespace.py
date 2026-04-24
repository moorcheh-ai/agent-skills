#!/usr/bin/env python3
"""Create a new Moorcheh namespace."""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from moorcheh_conn import get_client

def main():
    parser = argparse.ArgumentParser(description="Create a Moorcheh namespace")
    parser.add_argument("--name", required=True, help="Namespace name")
    parser.add_argument("--type", required=True, choices=["text", "vector"], help="Namespace type")
    parser.add_argument("--dimension", type=int, help="Vector dimension (required for vector type)")
    args = parser.parse_args()

    if args.type == "vector" and not args.dimension:
        print("Error: --dimension is required for vector namespaces")
        sys.exit(1)

    client = get_client()
    try:
        kwargs = {"namespace_name": args.name, "type": args.type}
        if args.dimension:
            kwargs["vector_dimension"] = args.dimension
        client.namespaces.create(**kwargs)
        print(f"[OK] Namespace '{args.name}' created successfully (type: {args.type})")
    except Exception as e:
        print(f"[ERROR] Error creating namespace: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
