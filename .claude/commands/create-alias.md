# /create-alias - Add Entity to Alias Mapping

Add a new entity (person, organization, location) to the persistent alias mapping.

## Workflow

1. **Load existing mapping** from `/aliases/active_mapping.json`
2. **Prompt for details**:
   - Original name/term
   - Alias/pseudonym to use
   - Entity type (person, organization, location, other)
   - Optional notes
3. **Check for conflicts**: Ensure alias isn't already in use
4. **Save updated mapping**

## Mapping File Structure

```json
{
  "version": "1.0",
  "created": "2024-01-15T10:00:00Z",
  "updated": "2024-01-15T10:00:00Z",
  "entities": [
    {
      "original": "John Smith",
      "alias": "Source A",
      "type": "person",
      "variations": ["John", "J. Smith", "Mr. Smith"],
      "notes": "Primary whistleblower"
    },
    {
      "original": "Acme Corporation",
      "alias": "Organization X",
      "type": "organization",
      "variations": ["Acme Corp", "Acme", "ACME"],
      "notes": ""
    }
  ]
}
```

## Example Invocation

User: `/create-alias`

Claude: I'll add a new entity to your alias mapping.

**What is the original name or term?**
> John Smith

**What alias should replace it?**
> Source A

**What type of entity is this?**
1. Person
2. Organization
3. Location
4. Other

> 1

**Any variations to also replace?** (comma-separated, or leave blank)
> John, J. Smith, Mr. Smith, Smith

**Any notes to add?** (optional)
> Primary source for financial documents

Added to mapping:
- "John Smith" (and variations) -> "Source A"

The alias will be applied when using consistent alias mode in /redact.

## Notes

- Aliases are stored in `/aliases/active_mapping.json`
- Multiple mapping files can exist for different projects
- Use `/show-mapping` to view current aliases
- Use `/import-schema` to load mappings from another project
