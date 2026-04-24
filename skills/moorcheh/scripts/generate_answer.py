#!/usr/bin/env python3
"""Generate AI-powered answers from Moorcheh namespace data (RAG)."""

import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from moorcheh_conn import get_client

def main():
    parser = argparse.ArgumentParser(description="Generate AI answers from Moorcheh data")
    parser.add_argument("--namespace", required=True, help="Namespace to search for context")
    parser.add_argument("--query", required=True, help="Question to answer")
    parser.add_argument("--top-k", type=int, default=5, help="Number of context documents (default: 5)")
    parser.add_argument("--temperature", type=float, help="Response creativity (0.0-2.0)")
    parser.add_argument("--model", default="anthropic.claude-sonnet-4-6", help="AI model ID (default: anthropic.claude-sonnet-4-6)")
    args = parser.parse_args()

    client = get_client()
    try:
        kwargs = {
            "namespace": args.namespace,
            "query": args.query,
            "top_k": args.top_k,
            "aiModel": args.model
        }
        if args.temperature is not None:
            kwargs["temperature"] = args.temperature

        response = client.answer.generate(**kwargs)

        print(f"Question: {args.query}\n")
        print(f"Answer: {response.get('answer', 'No answer generated')}\n")
        print(f"Model: {response.get('model', 'unknown')}")
        print(f"Context documents used: {response.get('contextCount', 0)}")
    except Exception as e:
        print(f"❌ Error generating answer: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
