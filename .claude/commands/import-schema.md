# /import-schema - Import Existing Redaction Schema

Import a previously exported redaction schema to apply consistent redaction.

## Workflow

1. **Locate schema file**: Check `/schemas/` or user-specified path
2. **Validate format**: Ensure schema is properly formatted
3. **Preview contents**: Show what will be imported
4. **Merge strategy**: Handle conflicts with existing mapping
   - Overwrite existing
   - Skip conflicts
   - Merge (keep both)
5. **Import to active mapping**

## Supported Import Formats

- JSON schema (exported from this workspace)
- CSV mapping file
- Plain text mapping (parsed format)

## Example Invocation

User: `/import-schema`

Claude: I'll help you import a redaction schema.

**Available schema files in /schemas/:**
1. export_2024-01-10_project_alpha.json
2. mapping_backup.json
3. [Enter custom path]

> 1

**Preview of import:**
| Original | Alias | Type |
|----------|-------|------|
| John Smith | Source A | person |
| Acme Corp | Org X | organization |

**3 entities will be imported.**

**Conflict detected:** "Acme Corp" already exists in active mapping with alias "Organization X"

How should I handle this?
1. Keep existing (Acme Corp -> Organization X)
2. Overwrite with import (Acme Corp -> Org X)
3. Keep both under different aliases

> 1

Imported 2 entities (1 skipped due to conflict).
Active mapping updated.

## Use Cases

- Resuming a redaction project
- Applying consistent aliases across document batches
- Team sharing of redaction standards
- Backup restoration
