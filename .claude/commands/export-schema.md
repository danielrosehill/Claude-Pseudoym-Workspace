# /export-schema - Export Redaction Schema

Export the redaction mapping (what was replaced with what) for secure storage or sharing.

## Workflow

1. **Select source**: Choose which mapping to export
   - Active alias mapping (`/aliases/active_mapping.json`)
   - Document-specific mapping from `/schemas/`
2. **Choose format**:
   - JSON (full detail, machine-readable)
   - CSV (spreadsheet compatible)
   - Plain text (human readable, printable)
   - Encrypted JSON (for secure storage)
3. **Generate export file**
4. **Provide security reminder**

## Export Formats

### JSON (default)
```json
{
  "export_date": "2024-01-15T10:00:00Z",
  "source_file": "active_mapping.json",
  "entities": [...]
}
```

### CSV
```csv
Original,Alias,Type,Variations
John Smith,Source A,person,"John, J. Smith"
Acme Corp,Organization X,organization,"Acme, ACME"
```

### Plain Text
```
REDACTION SCHEMA EXPORT
Date: 2024-01-15

PEOPLE:
  John Smith -> Source A
  Jane Doe -> Source B

ORGANIZATIONS:
  Acme Corporation -> Organization X
```

## Example Invocation

User: `/export-schema`

Claude: I'll export your redaction mapping.

**What would you like to export?**
1. Active alias mapping (current working set)
2. Specific document schema
3. All schemas

> 1

**Export format?**
1. JSON (recommended for reimport)
2. CSV (for spreadsheets)
3. Plain text (for printing/reference)

> 1

Exported to: `/schemas/export_2024-01-15_active_mapping.json`

**SECURITY REMINDER**: This file contains the key to re-identifying redacted entities. Store it securely:
- Encrypt if storing digitally
- Consider physical storage for high-security cases
- Destroy after verification if re-identification should be impossible
