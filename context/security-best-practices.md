# Security Best Practices for Document Redaction

## Threat Model Considerations

Before redacting, consider your threat model:

### Questions to Ask

1. **Who is the adversary?**
   - Casual observer
   - Employer/organization
   - Law enforcement
   - Nation-state actor

2. **What are they trying to learn?**
   - Identity of source
   - Location of events
   - Timeline of activities
   - Relationships between people

3. **What resources do they have?**
   - Basic search capabilities
   - Data correlation tools
   - Forensic analysis capabilities
   - Access to other data sources

4. **What are the consequences of failure?**
   - Embarrassment
   - Job loss
   - Legal action
   - Physical safety risk

## Operational Security (OPSEC)

### Before You Begin

1. **Air-gapped processing**: For highest security, process documents on a computer not connected to the internet
2. **Secure workspace**: Ensure no one can observe your screen
3. **Verify tool integrity**: Use trusted sources for all software
4. **Disable cloud sync**: Ensure documents aren't auto-uploaded anywhere

### During Processing

1. **Single session**: Complete redaction in one session if possible
2. **No copy-paste to web**: Don't paste sensitive text into web tools for any reason
3. **Monitor clipboard**: Clear clipboard after pasting sensitive data
4. **Disable auto-save**: Prevent intermediate versions being saved

### After Processing

1. **Secure deletion**: Don't just delete originals - use secure deletion
   ```bash
   shred -vfz -n 5 sensitive_file.txt
   ```
2. **Clear temporary files**: Many applications create temp files
3. **Clear recent files**: Remove from "recently opened" lists
4. **Verify nothing remains**: Search file system for fragments

## Common Mistakes

### 1. Incomplete Redaction

**Problem**: Black boxes over text in PDF that can be copy-pasted

**Solution**: Ensure redaction flattens or removes underlying text
```bash
# Wrong: Just adding black rectangles
# Right: Use proper PDF redaction that removes text
qpdf --flatten-annotations=all input.pdf output.pdf
```

### 2. Reversible Changes

**Problem**: Using Word's highlighter or text color change instead of deletion

**Solution**: Actually delete or replace text, don't just hide it

### 3. Forgetting Metadata

**Problem**: Redacting document content but leaving "Author: John Smith" in properties

**Solution**: Always scrub metadata after content redaction

### 4. Inconsistent Redaction

**Problem**: Redacting "John" as "[NAME]" but missing "John's" or "Johns"

**Solution**:
- Search for all variations
- Use stemming in search
- Review manually after automated processing

### 5. Contextual Leakage

**Problem**: "The CEO called [REDACTED] about the Seattle office" - if there's only one Seattle office, identity may be obvious

**Solution**: Consider context and chain of inference

### 6. Unique Phrases

**Problem**: Leaving unique phrases that can be searched

**Solution**: Search for unusual phrases and consider their searchability

### 7. Embedded Objects

**Problem**: Redacting document but leaving embedded Excel sheet with sensitive data

**Solution**: Check for and process all embedded objects

### 8. Version History

**Problem**: Sharing .docx with track changes still visible

**Solution**: Accept all changes and disable tracking before sharing

### 9. PDF Layers

**Problem**: Some PDFs have multiple layers; redacting visible layer leaves others

**Solution**: Flatten PDF before or after redaction

### 10. Filename and Path

**Problem**: Sending "C:\Users\JohnSmith\Documents\whistleblower_report.pdf"

**Solution**: Rename files and ensure paths don't reveal information

## Re-identification Attacks

### Direct Identifiers
- Name, SSN, email, phone
- **Mitigation**: Must be fully redacted

### Quasi-Identifiers
- Age, ZIP code, profession, dates
- **Mitigation**: Generalize or suppress combinations

### Narrative Details
- Unique events ("the day the printer caught fire")
- **Mitigation**: Review narrative for uniquely identifying events

### Writing Style
- Vocabulary, sentence structure
- **Mitigation**: Consider having someone else rewrite if style is a risk

### Timing Correlation
- "Email sent 3:47 PM on Tuesday" + server logs = identification
- **Mitigation**: Shift times or generalize to time ranges

## Verification Protocol

### Automated Checks
1. Search for all original sensitive terms
2. Search for variations and misspellings
3. Verify metadata removal
4. Check for embedded objects
5. Validate file format integrity

### Manual Review
1. Read redacted document completely
2. Consider: "If I knew the source, could I identify them from this?"
3. Consider: "What could an adversary correlate this with?"
4. Have second person review if possible

### Red Team Testing
For high-stakes scenarios:
1. Give redacted document to trusted party
2. Ask them to try to identify the source
3. Provide them similar context adversary would have
4. Iterate on redaction based on findings

## Document Distribution

### Secure Transmission
- Use encrypted channels (Signal, encrypted email)
- Don't use regular email for sensitive redacted documents
- Consider document watermarking to track leaks

### Access Control
- Limit who receives the document
- Consider need-to-know basis
- Track distribution if appropriate

### Persistence
- Assume once shared, document is permanent
- Consider what happens if document is leaked further
- Plan for worst-case disclosure

## Emergency Procedures

### If Original is Accidentally Shared
1. Immediately notify affected parties
2. Request deletion from recipients
3. Monitor for public appearance
4. Document incident for future reference

### If Redaction is Found to be Insufficient
1. Issue updated redacted version
2. Request destruction of prior version
3. Assess what information was exposed
4. Notify affected parties if necessary

## Legal Considerations

**Note**: This is not legal advice. Consult appropriate legal counsel.

- Redaction does not change legal discovery obligations
- Some jurisdictions have specific redaction requirements
- Consider attorney-client privilege implications
- Document your redaction process for potential legal review
