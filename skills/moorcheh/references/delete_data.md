# Delete Data

Delete specific documents or vectors from a namespace by ID. Use **`documents.delete`** for text namespaces and **`vectors.delete`** for vector namespaces. Deletions are permanent and decrement your item count.

**Warning:** This operation cannot be undone. Confirm IDs before calling.

Documentation index: [llms.txt](https://docs.moorcheh.ai/llms.txt).

---

## Python SDK: `documents.delete` / `vectors.delete`

Deletes items by ID. Text data → `client.documents.delete`; vector embeddings → `client.vectors.delete`.

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | `str` | Yes | Target namespace |
| `ids` | `list[str \| int]` | Yes | Document or vector IDs to delete (max **1000** per call). Numbers are converted to strings server-side |

**Returns:** `dict[str, Any]`- deletion status and counts (see below).

**Raises:** `NamespaceNotFound`, `InvalidInputError` (and other SDK/HTTP errors as applicable).

### Examples

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient() as client:
    result = client.documents.delete(
        namespace_name="my-faq-documents",
        ids=["faq-1", "faq-3", "faq-5"],
    )
    print(f"Deletion result: {result}")
```

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient() as client:
    result = client.vectors.delete(
        namespace_name="my-image-embeddings",
        ids=["image_001.jpg", "image_002.jpg"],
    )
    print(f"Deletion result: {result}")
```

### Response structure

The returned dict includes:

- `status` (`str`): `"success"` or `"partial"`
- `message` (`str`): Human-readable summary
- `requested_deletions` (`int`): Number of IDs in the request
- `actual_deletions` (`int`): Number of items actually removed
- `remaining_items` (`int`): Items left in the namespace after the operation
- `unprocessed_ids` (`list`, optional): IDs that failed to delete (partial success)

The underlying HTTP layer may return **200** when no items failed to process, or **207** when some IDs could not be deleted; the SDK surfaces this via `status` and `unprocessed_ids`.

### Complete example

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient() as client:
    namespace = "my-documents"
    ids_to_delete = ["doc-1", "doc-2", "doc-3", "doc-4", "doc-5"]

    result = client.documents.delete(
        namespace_name=namespace,
        ids=ids_to_delete,
    )

    print(f"Requested deletions: {result.get('requested_deletions', 0)}")
    print(f"Actual deletions: {result.get('actual_deletions', 0)}")
    print(f"Remaining items: {result.get('remaining_items', 0)}")

    if result.get("status") == "partial":
        unprocessed = result.get("unprocessed_ids", [])
        if unprocessed:
            print(f"Failed to delete: {unprocessed}")
```

### SDK: important notes

- At most **1,000** IDs per request; batch larger jobs.
- IDs may be strings or integers; they are normalized to strings internally.
- Use `documents.delete` for text namespaces and `vectors.delete` for vector namespaces.
- The namespace must exist and belong to your account.

### Understanding responses

- Prefer comparing **`actual_deletions`** to **`requested_deletions`** to see how many matched real items.
- If **`actual_deletions`** is `0`, the IDs may not exist in that namespace.
- **`remaining_items`** reflects namespace size after the call.

### Best practices

- Resolve IDs (e.g. via Get Documents) before deleting.
- Batch deletes for large cleanups; inspect each response.
- Handle **`status == "partial"`** and retry or log `unprocessed_ids` as needed.
- Back up or export important data before bulk deletion.

### Related (Python SDK)

- [Get Documents](https://docs.moorcheh.ai/python-sdk/data/get-documents.md)
- [Upload Text Data](https://docs.moorcheh.ai/python-sdk/data/upload-text.md)
- [Upload Vector Data](https://docs.moorcheh.ai/python-sdk/data/upload-vector.md)

---

## REST API (same behavior)

For raw HTTP clients:

- **Text documents:** `POST https://api.moorcheh.ai/v1/namespaces/{namespace_name}/documents/delete`
- **Vector embeddings:** `POST https://api.moorcheh.ai/v1/namespaces/{namespace_name}/vectors/delete`

**Headers:** `Content-Type: application/json`, `x-api-key: <key>`.

### Request body

| Field | Type | Required | Description |
|---|---|---|---|
| `ids` | array of string \| number | Yes | Non-empty; max **1000** ids per call (same as SDK) |

```json
{ "ids": ["document-001", "document-002"] }
```

### Responses (typical)

**200- all ids processed with no failures:**

```json
{
  "status": "success",
  "message": "3 documents deleted successfully from namespace 'my-namespace'.",
  "namespace_name": "my-namespace",
  "requested_deletions": 3,
  "actual_deletions": 3,
  "remaining_items": 997,
  "unprocessed_ids": []
}
```

**207- partial (some ids missing, wrong type, or server-side skip):**

```json
{
  "status": "partial",
  "message": "2 of 3 items deleted; 1 id was not found.",
  "namespace_name": "my-namespace",
  "requested_deletions": 3,
  "actual_deletions": 2,
  "remaining_items": 998,
  "unprocessed_ids": ["ghost-doc-id"]
}
```

The SDK maps the same fields; rely on **`status`**, **`actual_deletions`**, and **`unprocessed_ids`** for control flow.

**Vector delete** responses use the same field names (`requested_deletions`, `actual_deletions`, `remaining_items`, `unprocessed_ids`).

### Errors (examples)

```json
{
  "error": "Namespace not found",
  "message": "No namespace found with the name 'my-namespace'.",
  "namespace_name": "my-namespace"
}
```

```json
{
  "status": "failure",
  "message": "Bad Request: ids must be a non-empty array with at most 1000 elements."
}
```

**Delete documents:**

```bash
curl -X POST "https://api.moorcheh.ai/v1/namespaces/my-namespace/documents/delete" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{"ids": ["document-001", "document-002"]}'
```

**Delete vectors:**

```bash
curl -X POST "https://api.moorcheh.ai/v1/namespaces/my-vector-namespace/vectors/delete" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{"ids": ["vector-123", "vector-456"]}'
```

---

## Use cases

- Data cleanup and content management
- Privacy or compliance deletes by known ID
- Storage management and test teardown

To remove an entire namespace (all data and the namespace itself), use [Delete Namespace](delete_namespace.md).

To remove **uploaded storage files by file name** (not indexed IDs), use [Delete Files](delete_files.md).

To **fetch indexed documents by ID** before deleting chunks, use [Get Documents](get_documents.md).

## Official references

- [Delete Data- Python SDK](https://docs.moorcheh.ai/python-sdk/data/delete.md)
- [Delete Data- REST](https://docs.moorcheh.ai/api-reference/data/delete.md)
