[![Claude Code Repos Index](https://img.shields.io/badge/Claude%20Code%20Repos-Index-blue?style=flat-square&logo=github)](https://github.com/danielrosehill/Claude-Code-Repos-Index)

# Pseudonym Workspace

A Claude Code workspace for information security and document redaction, designed to protect the identity of whistleblowers, journalists' sources, research participants, and anyone handling sensitive information.

## Purpose

This workspace provides tools and workflows for:

- **Document Redaction**: Replace names, organizations, locations, and other identifying information with pseudonyms
- **Metadata Scrubbing**: Remove hidden metadata from images, PDFs, and documents that could reveal origins
- **Pattern Detection**: Automatically identify and redact emails, phone numbers, addresses, and other sensitive patterns
- **Alias Management**: Maintain consistent pseudonym mappings across document sets
- **Verification**: Check that redaction is complete and consistent

## Quick Start

1. Place documents in `/input/`
2. Run `/analyze` to identify sensitive information
3. Create or import an alias mapping
4. Run `/redact` with your chosen technique
5. Run `/scrub-metadata` on output files
6. Run `/verify-redaction` to check completeness
7. Export mapping schema for secure storage (if needed)

## Available Commands

| Command | Description |
|---------|-------------|
| `/redact` | Interactive document redaction |
| `/analyze` | Scan for sensitive information |
| `/scrub-metadata` | Remove file metadata |
| `/create-alias` | Add entity to alias mapping |
| `/show-mapping` | Display current aliases |
| `/export-schema` | Export redaction mapping |
| `/import-schema` | Import existing mapping |
| `/verify-redaction` | Check redaction completeness |

## Redaction Techniques

### Consistent Alias Mode
Use when the same pseudonym should appear throughout all documents:
- "John Smith" → "Source A" everywhere
- Maintains relationships between documents
- Best for: Legal documents, journalism, coordinated releases

### Random Replacement Mode
Use when documents should not be correlatable:
- "John Smith" → "ID-7X9K2M1P" (unique per document)
- Maximum protection against cross-referencing
- Best for: High-security situations, source protection

### Pattern-Based Mode
Automatic detection and redaction:
- Emails → `[EMAIL-REDACTED-001]`
- Phones → `[PHONE-REDACTED-001]`
- SSNs → `[SSN-REDACTED]`
- Best for: Bulk processing, data cleanup

### Hybrid Mode
Combine techniques for comprehensive protection:
- Named entities get consistent aliases
- Contact information gets pattern redaction
- Best for: Most real-world scenarios

## Directory Structure

```
/input/           # Documents to be redacted (not tracked by git)
/output/          # Redacted documents (not tracked by git)
/schemas/         # Mapping templates and examples
/aliases/         # Active alias mappings
/scripts/         # Python tools for processing
/context/         # Reference documentation
/.claude/commands/  # Slash command definitions
```

## Python Tools

Standalone tools that can be used outside of Claude Code:

### text_redactor.py
```bash
python scripts/text_redactor.py input.txt output.txt --mapping aliases/active_mapping.json
python scripts/text_redactor.py input.txt --analyze  # Analyze without redacting
```

### metadata_scrubber.py
```bash
python scripts/metadata_scrubber.py photo.jpg          # Scrub image metadata
python scripts/metadata_scrubber.py document.pdf       # Scrub PDF metadata
python scripts/metadata_scrubber.py file.jpg --verify  # Check if clean
```

### alias_manager.py
```bash
python scripts/alias_manager.py mapping.json list                    # List all entities
python scripts/alias_manager.py mapping.json add "John Smith" "Source A" --type person
python scripts/alias_manager.py mapping.json export output.csv       # Export to CSV
```

## System Requirements

For full functionality, install:

```bash
# Ubuntu/Debian
sudo apt install exiftool qpdf ffmpeg mat2 imagemagick

# Check tool availability
python scripts/metadata_scrubber.py --check-tools
```

## Security Considerations

### What This Workspace Does
- Processes documents locally
- Creates reversible mappings (if you choose to save them)
- Provides tools for systematic redaction

### What It Does NOT Do
- Guarantee anonymization (always review manually)
- Store original documents (clear /input/ after processing)
- Transmit data to external services

### Best Practices
1. **Air-gap for sensitive work**: Use offline computer for highest security
2. **Destroy mappings**: If re-identification should be impossible, securely delete mapping files
3. **Review output**: Automated redaction cannot catch all contextual risks
4. **Consider writing style**: Unique phrasing can identify sources
5. **Test first**: Verify workflow with non-sensitive test documents

## Use Cases

### Whistleblower Document Preparation
Protect identity when sharing evidence with journalists or authorities.

### Academic Research Anonymization
Comply with IRB requirements for participant privacy.

### Journalistic Source Protection
Redact documents before publication to protect sources.

### Legal Discovery
Remove privileged or sensitive information before document production.

### Data Sanitization
Clean datasets for sharing or publication.

## Contributing

This is a Claude Space - a specialized workspace for Claude Code. The structure follows the Claude Spaces model for organizing AI-assisted workflows.

## License

MIT License - See LICENSE file for details.

---

**Important**: This tool assists with redaction but does not guarantee anonymity. Always:
- Review output documents manually
- Consider contextual re-identification risks
- Consult security professionals for high-stakes situations
- Follow applicable legal and ethical guidelines

---

For more Claude Code projects, visit my [Claude Code Repos Index](https://github.com/danielrosehill/Claude-Code-Repos-Index).
