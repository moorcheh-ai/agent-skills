# Delete Data

Remove specific documents or all data from a namespace.

## API

```
DELETE https://api.moorcheh.ai/v1/namespaces/{namespace_name}/data
```

### Delete Specific Documents

```bash
curl -X DELETE "https://api.moorcheh.ai/v1/namespaces/my-documents/data" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "ids": ["doc-001", "doc-002"]
  }'
```

### Delete All Data

```bash
curl -X DELETE "https://api.moorcheh.ai/v1/namespaces/my-documents/data" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $MOORCHEH_API_KEY" \
  -d '{
    "delete_all": true
  }'
```

## Python SDK

```python
from moorcheh_sdk import MoorchehClient

with MoorchehClient(api_key="your-api-key") as client:
    # Delete specific documents
    client.documents.delete(
        namespace_name="my-documents",
        ids=["doc-001", "doc-002"]
    )
```

## Important Notes

- Deleting data is **irreversible**
- Always confirm with the user before deleting
- To delete the entire namespace (including the namespace itself), use the Delete Namespace operation instead
