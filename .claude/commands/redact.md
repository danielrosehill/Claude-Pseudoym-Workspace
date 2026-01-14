# /redact - Interactive Document Redaction

Perform interactive redaction on documents in the `/input/` directory.

## Workflow

1. **List input files**: Check `/input/` for documents to process
2. **Analyze content**: Identify sensitive information types present
3. **Confirm technique**: Ask user which redaction method to use:
   - Consistent aliases (same pseudonym throughout)
   - Random replacement (unique IDs per document)
   - Pattern-based (automatic detection of emails, phones, etc.)
   - Hybrid (combination of above)

4. **Execute redaction**: Process documents according to selected technique
5. **Generate mapping**: If requested, create schema showing original -> redacted mapping
6. **Output results**: Place redacted documents in `/output/`

## User Interaction Required

Ask the user:
1. Which files to process (or all)
2. What entities/patterns need redaction
3. Which technique to apply
4. Whether to generate a mapping schema
5. Whether to also scrub metadata

## Output

- Redacted documents in `/output/`
- Optional mapping schema in `/schemas/`
- Summary of what was redacted

## Example Invocation

User: `/redact`

Claude: I found the following files in /input/:
- interview_transcript.txt
- source_document.pdf

What would you like to redact? (e.g., "all names", "emails and phone numbers", "specific entities")

[User responds with requirements]

Claude: Which redaction technique should I use?
1. **Consistent aliases** - Same pseudonym for each entity across all documents
2. **Random replacement** - Unique identifier for each entity in each document
3. **Pattern-based** - Automatic detection and replacement of common patterns
4. **Hybrid** - Names get aliases, contact info gets pattern redaction

[Proceeds based on user selection]
