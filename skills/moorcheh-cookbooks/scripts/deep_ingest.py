#!/usr/bin/env python3
"""Deep Ingest helper: create staging namespace, upload file, or cleanup."""

import argparse
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "moorcheh", "scripts"))
from moorcheh_conn import get_client


def stage(client, file_path, namespace):
    """Create staging namespace and upload file."""
    if not os.path.isfile(file_path):
        print(f"[ERROR] File not found: {file_path}")
        sys.exit(1)

    print(f"Creating staging namespace '{namespace}'...")
    client.namespaces.create(namespace_name=namespace, type="text")
    print("[OK] Staging namespace created")

    print(f"Uploading '{file_path}' to staging namespace...")
    client.documents.upload_file(namespace_name=namespace, file_path=file_path)
    print("[OK] File uploaded")

    print("[WAIT] Waiting 15s for Moorcheh to extract, chunk, and index...")
    time.sleep(15)
    print(f"[OK] Staging ready. Query namespace '{namespace}' to discover document structure.")


def cleanup(client, namespace):
    """Delete staging namespace."""
    client.namespaces.delete(namespace_name=namespace)
    print(f"[OK] Staging namespace '{namespace}' deleted")


def main():
    parser = argparse.ArgumentParser(description="Deep Ingest: stage large/binary files via Moorcheh")
    parser.add_argument("--file", help="Path to file to ingest (PDF, DOCX, XLSX, TXT, CSV, JSON, MD)")
    parser.add_argument("--staging-namespace", help="Staging namespace name (e.g. staging-big-report)")
    parser.add_argument("--cleanup", metavar="NAMESPACE", help="Delete a staging namespace after use")
    args = parser.parse_args()

    if not args.file and not args.cleanup:
        parser.print_help()
        sys.exit(1)

    client = get_client()

    try:
        if args.cleanup:
            cleanup(client, args.cleanup)
        elif args.file and args.staging_namespace:
            stage(client, args.file, args.staging_namespace)
        else:
            print("[ERROR] --file requires --staging-namespace")
            sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
