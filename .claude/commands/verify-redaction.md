# /verify-redaction - Verify Redaction Completeness

Check redacted documents for potential issues, missed redactions, or inconsistencies.

## Workflow

1. **Load mapping**: Get current alias mapping
2. **Scan output documents**: Read files from `/output/`
3. **Check for originals**: Search for any original terms that should have been redacted
4. **Check consistency**: Verify same entity always maps to same alias
5. **Check metadata**: Verify metadata has been removed
6. **Check for inferential risks**: Flag potential re-identification vectors
7. **Generate verification report**

## Checks Performed

### Direct Checks
- [ ] Original names/terms not present in output
- [ ] No partial matches (e.g., "John" when "John Smith" was redacted)
- [ ] No variations missed (e.g., "J. Smith" when "John Smith" was redacted)
- [ ] Consistent alias usage throughout
- [ ] Metadata removed

### Pattern Checks
- [ ] No unredacted email addresses
- [ ] No unredacted phone numbers
- [ ] No unredacted SSNs/IDs
- [ ] No unredacted addresses

### Contextual Checks
- [ ] No highly specific job titles + organization combinations
- [ ] No unique event descriptions
- [ ] No timestamps that could correlate with logs

## Output Format

```
## Verification Report

**Documents checked**: 3
**Status**: ISSUES FOUND

### document1_redacted.txt
- PASS: No original terms found
- PASS: Metadata clean
- WARNING: Found "the CEO" - could narrow identification

### document2_redacted.pdf
- FAIL: Found "john.smith" (partial email match)
- PASS: Metadata clean
- PASS: No other issues

### Summary
- Documents with issues: 1
- Critical issues: 1 (partial match found)
- Warnings: 1 (contextual concern)

### Recommended Actions
1. Re-redact document2_redacted.pdf to catch email fragment
2. Consider generalizing "the CEO" to "[EXECUTIVE]" in document1
```

## Example Invocation

User: `/verify-redaction`

Claude: I'll verify the redacted documents against the mapping.

**Checking /output/ against active mapping...**

[Runs verification checks]

## Verification Report

**Documents checked**: 2
**Status**: ALL CLEAR

### interview_redacted.txt
- All original entities successfully redacted
- No partial matches found
- No pattern matches found
- Metadata: N/A (plain text)

### source_doc_redacted.pdf
- All original entities successfully redacted
- No partial matches found
- No pattern matches found
- Metadata: Clean (verified with exiftool)

All documents pass verification.

**Reminder**: Automated verification cannot catch all risks. Manual review is still recommended, especially for:
- Contextual details that could enable inference
- Unique phrases or events
- Writing style identification
