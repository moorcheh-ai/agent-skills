#!/usr/bin/env python3
"""Perform semantic search across Moorcheh namespaces."""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from moorcheh_conn import get_client

def main():
    parser = argparse.ArgumentParser(description="Search Moorcheh namespaces")
    parser.add_argument("--query", required=True, help="Search query text")
    parser.add_argument("--namespaces", required=True, help="Comma-separated namespace names")
    parser.add_argument("--top-k", type=int, default=10, help="Number of results (default: 10)")
    parser.add_argument("--threshold", type=float, help="Minimum relevance score (0.0-1.0)")
    args = parser.parse_args()

    namespaces = [ns.strip() for ns in args.namespaces.split(",")]

    client = get_client()
    try:
        kwargs = {
            "namespaces": namespaces,
            "query": args.query,
            "top_k": args.top_k
        }
        if args.threshold is not None:
            kwargs["threshold"] = args.threshold

        results = client.similarity_search.query(**kwargs)
        matches = results.get("results", [])

        if not matches:
            print("No results found.")
            return

        print(f"Found {len(matches)} result(s):\n")
        for i, match in enumerate(matches, 1):
            score = match.get("score", 0)
            label = match.get("label", "Unknown")
            text = match.get("text", "")[:200]
            doc_id = match.get("id", "?")
            print(f"  {i}. [{label}] (Score: {score:.4f})")
            print(f"     ID: {doc_id}")
            print(f"     {text}...")
            if match.get("metadata"):
                print(f"     Metadata: {match['metadata']}")
            print()

        exec_time = results.get("execution_time", 0)
        print(f"Execution time: {exec_time:.3f}s")
    except Exception as e:
        print(f"[ERROR] Error searching: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
