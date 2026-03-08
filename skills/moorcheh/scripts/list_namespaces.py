#!/usr/bin/env python3
"""List all Moorcheh namespaces."""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from moorcheh_conn import get_client

def main():
    client = get_client()
    try:
        namespaces = client.namespaces.list()
        if not namespaces:
            print("No namespaces found. Create one with create_namespace.py")
            return
        print(f"Found {len(namespaces)} namespace(s):\n")
        for ns in namespaces:
            ns_type = ns.get("type", "unknown")
            name = ns.get("namespace_name", "unnamed")
            print(f"  📁 {name} (type: {ns_type})")
            if ns_type == "vector":
                dim = ns.get("vector_dimension", "?")
                print(f"     Dimension: {dim}")
        print()
    except Exception as e:
        print(f"❌ Error listing namespaces: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
