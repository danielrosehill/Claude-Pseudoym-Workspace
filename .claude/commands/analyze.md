# /analyze - Sensitive Information Scanner

Scan documents for potentially sensitive information that may need redaction.

## Workflow

1. **Read documents** from `/input/` directory
2. **Detect sensitive patterns**:
   - Names (proper nouns, titles)
   - Email addresses
   - Phone numbers
   - Physical addresses
   - Social Security Numbers / National IDs
   - Financial information (account numbers, amounts)
   - Dates that could be identifying
   - Organization names
   - Location references
   - Unique identifying phrases

3. **Generate report**: Create a categorized list of findings
4. **Risk assessment**: Flag high-risk items
5. **Recommend techniques**: Suggest appropriate redaction methods

## Output Format

```
## Analysis Report for [filename]

### High Risk (Direct Identifiers)
- Names found: [list]
- Email addresses: [count] found
- Phone numbers: [count] found
- SSN/ID numbers: [count] found

### Medium Risk (Quasi-Identifiers)
- Addresses: [list]
- Dates: [list]
- Organizations: [list]
- Job titles: [list]

### Potential Concerns
- Unique phrases that could be searched: [list]
- Contextual details that narrow identification: [notes]

### Recommendations
- Suggested redaction technique: [recommendation]
- Special considerations: [notes]
```

## Example Invocation

User: `/analyze`

Claude: I'll scan the documents in /input/ for sensitive information.

[Reads documents]

## Analysis Report for interview_transcript.txt

### High Risk (Direct Identifiers)
- **Names found**: John Smith (12 occurrences), Jane Doe (8 occurrences), Acme Corporation (5 occurrences)
- **Email addresses**: 2 found (john.smith@acme.com, jdoe@gmail.com)
- **Phone numbers**: 1 found (555-123-4567)

### Medium Risk (Quasi-Identifiers)
- **Dates**: March 15, 2024 (3 occurrences)
- **Locations**: Chicago office, Building B

### Recommendations
- Use consistent alias mode for the named individuals
- Pattern redaction for email and phone
- Consider generalizing "Chicago office" to "[LOCATION]"

Would you like me to proceed with redaction using these findings?
