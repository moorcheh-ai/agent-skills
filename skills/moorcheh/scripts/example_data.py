#!/usr/bin/env python3
"""Create example data in a Moorcheh namespace for demos and testing."""

import argparse
import time
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from moorcheh_conn import get_client

SAMPLE_DOCUMENTS = [
    {
        "id": "demo-tech-1",
        "text": "Artificial intelligence is transforming healthcare through improved diagnostics, personalized treatment plans, and drug discovery. Machine learning models can analyze medical images with accuracy comparable to experienced radiologists.",
        "category": "technology",
        "author": "Dr. Chen",
        "difficulty": "beginner"
    },
    {
        "id": "demo-tech-2",
        "text": "Large language models like GPT and Claude represent a paradigm shift in natural language processing. These transformer-based models can understand context, generate human-like text, and perform complex reasoning tasks.",
        "category": "technology",
        "author": "Prof. Williams",
        "difficulty": "intermediate"
    },
    {
        "id": "demo-tech-3",
        "text": "Edge computing brings computation closer to data sources, reducing latency and bandwidth usage. Combined with IoT sensors, edge computing enables real-time processing for autonomous vehicles and smart manufacturing.",
        "category": "technology",
        "author": "Maria Lopez",
        "difficulty": "advanced"
    },
    {
        "id": "demo-science-1",
        "text": "Quantum computing leverages quantum mechanical phenomena like superposition and entanglement to process information in fundamentally new ways. Quantum computers excel at optimization problems and cryptographic challenges.",
        "category": "science",
        "author": "Prof. Johnson",
        "difficulty": "advanced"
    },
    {
        "id": "demo-science-2",
        "text": "CRISPR-Cas9 gene editing technology allows precise modifications to DNA sequences. This breakthrough enables potential treatments for genetic diseases and advances in agricultural biotechnology.",
        "category": "science",
        "author": "Dr. Patel",
        "difficulty": "intermediate"
    },
    {
        "id": "demo-business-1",
        "text": "Effective startup growth requires a balance of product-market fit, user acquisition, and sustainable unit economics. The lean startup methodology emphasizes rapid iteration and data-driven decision making.",
        "category": "business",
        "author": "Sarah Kim",
        "difficulty": "beginner"
    },
    {
        "id": "demo-business-2",
        "text": "Retrieval-Augmented Generation (RAG) is becoming essential for enterprise AI applications. By grounding AI responses in company-specific data, RAG reduces hallucinations and provides accurate, contextual answers.",
        "category": "business",
        "author": "James Park",
        "difficulty": "intermediate"
    }
]

def main():
    parser = argparse.ArgumentParser(description="Create example data in Moorcheh")
    parser.add_argument("--namespace", default="demo-namespace", help="Namespace name (default: demo-namespace)")
    parser.add_argument("--skip-create", action="store_true", help="Skip namespace creation")
    args = parser.parse_args()

    client = get_client()

    try:
        if not args.skip_create:
            print(f"Creating namespace '{args.namespace}'...")
            client.namespaces.create(namespace_name=args.namespace, type="text")
            print("[OK] Namespace created")

        print(f"Uploading {len(SAMPLE_DOCUMENTS)} sample documents...")
        client.documents.upload(
            namespace_name=args.namespace,
            documents=SAMPLE_DOCUMENTS
        )
        print(f"[OK] Uploaded {len(SAMPLE_DOCUMENTS)} documents")
        print("[WAIT] Waiting for indexing...")
        time.sleep(5)

        print("\nTesting search...")
        results = client.similarity_search.query(
            namespaces=[args.namespace],
            query="How is AI used in healthcare?"
        )
        matches = results.get("results", [])
        print(f"[OK] Search returned {len(matches)} results")
        if matches:
            top = matches[0]
            print(f"   Top result: [{top.get('label', '?')}] {top.get('text', '')[:80]}...")

        print(f"\n[OK] Demo data ready in namespace '{args.namespace}'")
        print("Try: /moorcheh:search query \"quantum computing\" namespaces \"" + args.namespace + "\"")
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
