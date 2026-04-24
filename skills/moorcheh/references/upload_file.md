# Upload File

Upload a file directly to a text namespace. Moorcheh handles parsing, chunking, embedding, and indexing automatically. **Prefer this over `upload_text` whenever the user has a file** — it avoids manual text extraction and large inline payloads.

## API

```
POST https://api.moorcheh.ai/v1/namespaces/{namespace_name}/upload_file
Content-Type: multipart/form-data
```

### Parameters

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file` | file | Yes | The file to upload (PDF, TXT, MD, CSV, JSON, DOCX) |

### Example

```bash
curl -X POST "https://api.moorcheh.ai/v1/namespaces/my-documents/upload_file" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -F "file=@report.pdf"
```

### Response

```json
{
  "status": "success",
  "message": "File uploaded successfully to namespace 'my-documents'",
  "upload_id": "upload_1234567890",
  "namespace_name": "my-documents",
  "file_name": "report.pdf",
  "processing_status": "in_progress"
}
```

## Python SDK

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    result = client.documents.upload_file(
        namespace_name="my-documents",
        file_path="report.pdf"
    )
    print(f"Uploaded: {result['file_name']}")
```

## Script

```bash
uv run skills/moorcheh/scripts/upload_file.py \
  --namespace "my-documents" \
  --file "report.pdf"
```

## When to use upload_file vs upload_text

| Scenario | Use |
|---|---|
| User has a file on disk (PDF, DOCX, CSV, etc.) | **upload_file** |
| User has structured JSON documents already in memory | upload_text |
| User wants automatic chunking and parsing | **upload_file** |
| User needs custom metadata per document | upload_text |

## Important Notes

- Files are processed **asynchronously** — allow time for parsing and indexing before searching
- Supported formats: PDF, TXT, MD, CSV, JSON, DOCX
- The namespace must be of type `"text"`
- Maximum file size depends on your Moorcheh plan
