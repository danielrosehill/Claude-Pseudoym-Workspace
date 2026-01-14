# Pseudonym Workspace - Information Security & Redaction

## Purpose

This Claude Space is designed to help protect the safety of whistleblowers, journalists, researchers, and anyone handling sensitive information that requires redaction or obfuscation before sharing.

## Core Capabilities

### Document Redaction
- **Text replacement**: Replace sensitive names, locations, organizations with pseudonyms
- **Consistent aliasing**: Maintain a mapping so "John Smith" always becomes "Mr. X" across documents
- **Random replacement**: Generate unique random identifiers per document for enhanced security
- **Pattern-based redaction**: Detect and redact emails, phone numbers, addresses, SSNs, etc.

### Metadata Scrubbing
- Remove EXIF data from images
- Strip document metadata (author, creation date, revision history)
- Clean PDF metadata and embedded information
- Sanitize file names and paths

### Security Analysis
- Identify potentially sensitive information in documents
- Highlight inconsistent redaction that could enable re-identification
- Detect hidden metadata that could compromise anonymity

## Workflow

1. **User provides input**: Place documents in `/input/` directory
2. **User specifies technique**: Describe what needs redaction and which method to use
3. **Claude processes**: Apply redaction according to specified technique
4. **Output generated**: Redacted documents placed in `/output/` with mapping schema if requested

## Redaction Techniques

### Consistent Alias Mode
Use when you need the same pseudonym throughout a document set:
- Maintains `/aliases/active_mapping.json` for persistent aliases
- Example: "Jane Doe" -> "Source A" across all documents

### Random Replacement Mode
Use for maximum security when documents shouldn't be cross-referenced:
- Generates unique identifiers per document
- Creates separate mapping file for each document
- Example: "Jane Doe" -> "P7X9-2K1M" (unique per document)

### Pattern Redaction Mode
Use for automated detection and replacement of sensitive patterns:
- Email addresses -> [EMAIL-REDACTED-001]
- Phone numbers -> [PHONE-REDACTED-001]
- Social Security Numbers -> [SSN-REDACTED]
- Addresses -> [ADDRESS-REDACTED-001]

### Hybrid Mode
Combine techniques for comprehensive protection:
- Named entities get consistent aliases
- Contact information gets pattern redaction
- Dates can be shifted by consistent offset

## Available Commands

| Command | Description |
|---------|-------------|
| `/redact` | Interactive redaction with technique selection |
| `/analyze` | Scan document for sensitive information |
| `/scrub-metadata` | Remove all metadata from files |
| `/create-alias` | Add new entity to alias mapping |
| `/show-mapping` | Display current alias mappings |
| `/export-schema` | Export redaction schema (input->output mapping) |
| `/import-schema` | Import existing redaction schema |
| `/verify-redaction` | Check for inconsistencies or missed redactions |

## Directory Structure

```
/input/           # Place documents to be redacted here
/output/          # Redacted documents appear here
/schemas/         # Redaction mapping schemas
/aliases/         # Persistent alias mappings
/scripts/         # Python tools for processing
/context/         # Reference documentation
/commands/        # Slash command definitions
```

## Security Considerations

### What This Space Does NOT Do
- Store original sensitive documents permanently
- Transmit data to external services (all processing is local)
- Guarantee 100% anonymization (always review output manually)

### Best Practices
1. **Always review output manually** - Automated redaction may miss context
2. **Test with non-sensitive data first** - Verify the workflow before using real documents
3. **Keep mapping schemas secure** - These are the key to re-identification
4. **Use random replacement for highest security** - When correlation between documents is a risk
5. **Clear /input/ after processing** - Don't leave sensitive documents in the workspace

## File Types Supported

### Text Documents
- `.txt`, `.md`, `.rtf`
- `.docx`, `.odt` (with metadata scrubbing)
- `.pdf` (text extraction and metadata removal)

### Images
- `.jpg`, `.jpeg`, `.png`, `.gif`, `.tiff`
- EXIF and metadata removal
- Optional face blurring (requires additional tools)

### Data Files
- `.csv`, `.json`, `.xml`
- Structured data redaction with schema preservation

## Example Workflows

### Whistleblower Document Preparation
1. Place documents in `/input/`
2. Run `/analyze` to identify sensitive information
3. Specify: "Replace all employee names with consistent aliases, redact all email addresses"
4. Run `/redact` with consistent alias mode
5. Run `/scrub-metadata` on output files
6. Run `/verify-redaction` to check for missed items
7. Export mapping schema for secure storage

### Academic Research Anonymization
1. Place interview transcripts in `/input/`
2. Create alias mapping: "Participant 1", "Participant 2", etc.
3. Run `/redact` with imported schema
4. Verify all identifying information removed

### Journalistic Source Protection
1. Place source documents in `/input/`
2. Use random replacement mode (no correlation between documents)
3. Run `/scrub-metadata`
4. Destroy mapping schemas after verification (no re-identification possible)

## Integration Notes

- Works with local file system only
- Can integrate with local LLMs for offline processing if needed
- Metadata scrubbing uses standard Linux tools (exiftool, qpdf, etc.)
- Python scripts for text processing are self-contained
