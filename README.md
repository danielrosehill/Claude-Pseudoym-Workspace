[![Claude Code Repos Index](https://img.shields.io/badge/Claude%20Code%20Repos-Index-blue?style=flat-square&logo=github)](https://github.com/danielrosehill/Claude-Code-Repos-Index)

# Claude Redaction and Obfuscation

A Claude Code workspace for document redaction, identity obfuscation, and information security. This workspace supports human-guided redaction workflows for sensitive use cases including whistleblowing, source protection, defamation defense, and anonymous publishing.

## What This Is (And Isn't)

**This is NOT** an automated PII detection/redaction tool. There are many excellent programmatic solutions for bulk PII scrubbing and compliance workflows.

**This IS** an interactive workspace for thoughtful, human-directed redaction where:
- You know what needs to be protected and why
- Context matters more than pattern matching
- Consistent obfuscation across documents is critical
- You need to maintain (or deliberately destroy) the ability to reverse the process

## Use Cases

### Whistleblowing & Source Protection
Prepare documents for disclosure while protecting your identity or your sources. Replace identifying details with consistent pseudonyms, strip metadata that could reveal document origins, and verify completeness before sharing.

### Defamation Protection
Sanitize documents for anonymous posting when discussing legally sensitive topics. Obfuscate identifying details about individuals or organizations to enable public discussion without liability exposure.

### Anonymous Publishing
Prepare content for publication where author identity must remain hidden. Remove stylometric fingerprints, strip metadata, and ensure no identifying breadcrumbs remain.

### Research & Journalism
Protect interview subjects, maintain source confidentiality, and comply with ethical requirements for participant privacy.

## Core Capabilities

- **Guided Redaction**: Interactive replacement of names, organizations, locations with pseudonyms or random identifiers
- **Metadata Scrubbing**: Remove EXIF, PDF metadata, document properties, and other hidden identifiers
- **Alias Management**: Maintain consistent mappings so "John Smith" always becomes "Source A" across your document set
- **Verification**: Check that redaction is complete and no identifying patterns slipped through

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

### Pattern-Assisted Mode
Claude can help identify common patterns, but you direct what gets redacted:
- Emails, phones, addresses flagged for your review
- You decide what's actually sensitive in context
- Best for: Catching items you might have missed

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

## When to Use This vs. Automated Tools

| Use This Workspace | Use Automated PII Tools |
|--------------------|------------------------|
| You know exactly what to redact | You need to scan unknown data for PII |
| Context determines what's sensitive | Regex patterns can identify the sensitive data |
| Consistency across documents matters | One-off bulk processing |
| You may need to reverse the redaction | Permanent, irreversible scrubbing is fine |
| Human judgment required | Compliance-driven automation |

## Contributing

This is a Claude Code workspace for human-guided redaction workflows. Contributions that improve the interactive redaction experience are welcome. This is explicitly not intended to become an automated PII detection tool.

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
