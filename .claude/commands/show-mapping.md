# /show-mapping - Display Current Alias Mappings

Display the current alias mapping configuration.

## Workflow

1. **Load mapping** from `/aliases/active_mapping.json`
2. **Format for display**: Show all entities and their aliases
3. **Include statistics**: Count of each entity type

## Output Format

```
## Current Alias Mapping

**File**: /aliases/active_mapping.json
**Last Updated**: 2024-01-15 10:00:00

### People (3 entries)
| Original | Alias | Variations |
|----------|-------|------------|
| John Smith | Source A | John, J. Smith, Mr. Smith |
| Jane Doe | Source B | Jane, J. Doe |
| Robert Johnson | Source C | Bob, Rob, R. Johnson |

### Organizations (2 entries)
| Original | Alias | Variations |
|----------|-------|------------|
| Acme Corporation | Organization X | Acme Corp, Acme, ACME |
| Beta Industries | Organization Y | Beta Inc |

### Locations (1 entry)
| Original | Alias | Variations |
|----------|-------|------------|
| 123 Main Street | [ADDRESS-1] | Main St office |

### Summary
- Total entities mapped: 6
- People: 3
- Organizations: 2
- Locations: 1
```

## Example Invocation

User: `/show-mapping`

Claude: Here is the current alias mapping:

[Displays formatted mapping table]

Would you like to:
1. Add a new alias (`/create-alias`)
2. Edit an existing alias
3. Delete an alias
4. Export this mapping (`/export-schema`)

## Options

- Show specific entity type only
- Show mapping from a different file
- Export to different format (CSV, plain text)
