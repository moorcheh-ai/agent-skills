# Upload File

Get a **pre-signed S3 URL** to upload large files directly (bypassing API Gateway’s **10MB** limit), then **PUT** bytes to S3. Moorcheh processes the object asynchronously (parse, chunk, embed, index).

**Prefer the Python SDK** `documents.upload_file` when you have a local path or file-like object- it requests the URL, uploads bytes, and you do not hand-roll HTTP.

Documentation index: [llms.txt](https://docs.moorcheh.ai/llms.txt).

---

## How it works (REST)

1. **POST** `…/upload-url` with JSON `{ "file_name": "…" }` → receive `upload_url`, `content_type`, `expires_in`, etc.
2. **PUT** the file bytes to `upload_url` with header `Content-Type` set to the returned `content_type`.
3. Backend **ingestion** runs after the S3 upload completes.

**Pre-signed URL expiry:** **15 minutes** (`expires_in` is typically **900** seconds). Request a new URL if it expires.

**Size limit:** up to **5GB** for this flow (per product docs).

---

## Step 1: Get pre-signed URL (REST)

### API

```
POST https://api.moorcheh.ai/v1/namespaces/{namespace_name}/upload-url
```

**Headers:** `Content-Type: application/json`, `x-api-key: <your-api-key>`

### Path parameters

| Name | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | string | Yes | Target **text** namespace |

### Body parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `file_name` | string | Yes | Target filename **with extension** (e.g. `document.pdf`). MIME type is inferred from the extension. |

Use **snake_case** (`file_name`). Legacy **`fileName`** may still be accepted with deprecation headers; prefer `file_name`- camelCase support is deprecated (scheduled removal **1 May 2026** per Moorcheh docs).

### Example

```bash
curl -X POST "https://api.moorcheh.ai/v1/namespaces/my-documents/upload-url" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"file_name": "document.pdf"}'
```

### 200 response

```json
{
  "upload_url": "https://s3.us-east-1.amazonaws.com/...",
  "key": "ownerId/namespace/document.pdf",
  "content_type": "application/pdf",
  "expires_in": 900,
  "method": "PUT",
  "hint": "Upload the file with: PUT <upload_url> with header Content-Type: application/pdf and body = file bytes"
}
```

| Field | Type | Description |
|---|---|---|
| `upload_url` | string | Pre-signed S3 URL for **PUT** |
| `key` | string | S3 object key |
| `content_type` | string | Use exactly this value as the **PUT** `Content-Type` header |
| `expires_in` | number | Seconds until URL expires (often **900**) |
| `method` | string | Always **PUT** |
| `hint` | string | Human-readable upload instructions |

### Errors (examples)

```json
{ "error": "file_name is required" }
```

```json
{
  "error": "File type '.exe' is not supported. Allowed types: .pdf, .docx, .xlsx, .json, .txt, .csv, .md"
}
```

```json
{ "error": "Unauthorized: API key is required" }
```

```json
{ "error": "Namespace 'example-namespace' not found" }
```

---

## Step 2: Upload bytes to S3 (REST)

```bash
curl -X PUT "<upload_url_from_step_1>" \
  -H "Content-Type: <content_type_from_step_1>" \
  --data-binary "@/path/to/document.pdf"
```

### Supported extensions and Content-Type

| Extension | Content-Type |
|-----------|----------------|
| `.pdf` | `application/pdf` |
| `.docx` | `application/vnd.openxmlformats-officedocument.wordprocessingml.document` |
| `.xlsx` | `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet` |
| `.json` | `application/json` |
| `.txt` | `text/plain` |
| `.csv` | `text/csv` |
| `.md` | `text/markdown` |

### Expired pre-signed URL (S3)

```xml
<Error>
  <Code>AccessDenied</Code>
  <Message>Request has expired</Message>
</Error>
```

Request a **new** upload URL from Step 1 and repeat the PUT.

---

## Python SDK: `documents.upload_file`

Uploads via the **pre-signed URL flow internally**: you do **not** need to call `upload-url` or S3 yourself.

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `namespace_name` | `str` | Yes | Target **text** namespace |
| `file_path` | `str` \| `Path` \| `BinaryIO` | Yes | Local path or readable binary file-like object |

**Returns:** `dict[str, Any]`- often includes fields such as `success`, `message`, `namespace`, `file_name`, `file_size` (exact keys depend on SDK/API version).

### Example response body (typical)

```json
{
  "success": true,
  "message": "File uploaded successfully and queued for processing.",
  "namespace": "my-faq-documents",
  "file_name": "document.pdf",
  "file_size": 245678
}
```

**Raises:** `NamespaceNotFound`, `InvalidInputError`, `AuthenticationError`, `APIError`, `MoorchehError`, etc.

### Example

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    status = client.documents.upload_file(
        namespace_name="my-faq-documents",
        file_path="C:/path/to/document.pdf",
    )
    print(status)
```

### Path or file-like object

```python
from pathlib import Path
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    result_a = client.documents.upload_file(
        namespace_name="my-faq-documents",
        file_path=Path("C:/path/to/guide.md"),
    )

    with open("C:/path/to/data.csv", "rb") as f:
        result_b = client.documents.upload_file(
            namespace_name="my-faq-documents",
            file_path=f,
        )

    print(result_a)
    print(result_b)
```

### End-to-end workflow

```python
from moorcheh_sdk import MoorchehClient
import time

with MoorchehClient(api_key="your-api-key") as client:
    client.namespaces.create(namespace_name="my-data", type="text")

    upload_result = client.documents.upload_file(
        namespace_name="my-data",
        file_path="C:/path/to/product-faq.pdf",
    )
    print(f"Upload response: {upload_result}")

    print("[WAIT] Waiting for file processing before search...")
    time.sleep(5)
```

## Important notes

- **Async processing**- allow time after upload before [Search](search.md) / [Generate AI Answer](generate_answer.md).
- **Supported types:** `.pdf`, `.docx`, `.xlsx`, `.json`, `.txt`, `.csv`, `.md` only.
- **Max file size:** **5GB** for this ingestion path.
- **Namespace type** must be **`text`**.

## Best practices

- Use stable, descriptive `file_name` values for auditing.
- Prefer structured markdown or plain text when you control the source format.
- Split very large corpora across multiple files when practical.
- Retry on transient network errors; refresh the pre-signed URL if S3 reports expiry.

## Script (SDK)

```bash
uv run skills/moorcheh/scripts/upload_file.py \
  --namespace "my-documents" \
  --file "report.pdf"

uv run skills/moorcheh/scripts/upload_file.py \
  --namespace "my-documents" \
  --dir "wiki/"
```

The script calls `client.documents.upload_file` (pre-signed flow under the hood).

## Upload file vs upload text

| Scenario | Use |
|---|---|
| File on disk (PDF, DOCX, XLSX, …) | **`documents.upload_file`** (SDK) or REST `upload-url` + S3 PUT |
| JSON document payloads already in memory | [Upload Text Data](upload_text.md) |
| Avoid reading file into the agent for upload | **SDK `upload_file`** or REST URL + PUT from disk |

## Related

- [Upload Text Data](upload_text.md)
- [List Files](list_files.md)- raw objects in storage after upload
- [Delete Files](delete_files.md)- remove storage objects by file name
- [Fetch Text Data](fetch_text_data.md)
- [Search](search.md)
- [Delete Data](delete_data.md)

## Official references

- [Upload File URL (REST)](https://docs.moorcheh.ai/api-reference/data/upload-file-url.md)
- [Upload File (Python SDK)](https://docs.moorcheh.ai/python-sdk/data/upload-file.md)
- [OpenAPI spec](https://docs.moorcheh.ai/api-reference/openapi.json) (search for `upload-url`, `delete-file`, `list-files`)
- [Documentation index](https://docs.moorcheh.ai/llms.txt)
- [Delete File (REST)](https://docs.moorcheh.ai/api-reference/data/delete-file.md)
- [Get Documents (REST)](https://docs.moorcheh.ai/api-reference/data/get-documents.md)
