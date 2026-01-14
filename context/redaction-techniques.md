# Redaction Techniques Reference

## Overview

This document provides detailed guidance on redaction techniques for protecting sensitive information while maintaining document utility.

## Technique Categories

### 1. Direct Replacement

**Description**: Replace sensitive text with a fixed placeholder or pseudonym.

**Use Cases**:
- Names of individuals
- Organization names
- Specific locations

**Example**:
```
Original: "John Smith met with Jane Doe at Acme Corp headquarters."
Redacted: "Source A met with Source B at Organization X headquarters."
```

**Pros**: Easy to implement, maintains readability
**Cons**: May allow correlation if same placeholder used across documents

### 2. Categorical Replacement

**Description**: Replace with category descriptors rather than specific placeholders.

**Use Cases**:
- When the category is relevant but specifics are not
- Academic research requiring demographic context

**Example**:
```
Original: "Dr. Sarah Chen, a 45-year-old neurologist from Stanford..."
Redacted: "[MEDICAL PROFESSIONAL], a [AGE RANGE: 40-50] [SPECIALTY] from [ACADEMIC INSTITUTION]..."
```

### 3. Pattern-Based Redaction

**Description**: Automatically detect and redact common sensitive patterns.

**Supported Patterns**:

| Pattern | Regex Example | Replacement |
|---------|---------------|-------------|
| Email | `[\w.-]+@[\w.-]+\.\w+` | [EMAIL-REDACTED] |
| Phone (US) | `\d{3}[-.]?\d{3}[-.]?\d{4}` | [PHONE-REDACTED] |
| SSN | `\d{3}-\d{2}-\d{4}` | [SSN-REDACTED] |
| Credit Card | `\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}` | [CC-REDACTED] |
| IP Address | `\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}` | [IP-REDACTED] |
| Date | `\d{1,2}/\d{1,2}/\d{2,4}` | [DATE-REDACTED] |

### 4. Date Shifting

**Description**: Shift all dates by a consistent offset to preserve temporal relationships.

**Use Cases**:
- Medical records where timeline matters
- Event sequences where duration is relevant

**Example**:
```
Offset: -47 days
Original: "Patient admitted January 15, 2024, discharged January 22, 2024"
Redacted: "Patient admitted November 29, 2023, discharged December 6, 2023"
```

### 5. Geographic Generalization

**Description**: Replace specific locations with broader geographic areas.

**Levels**:
1. Exact address -> Neighborhood
2. Neighborhood -> City
3. City -> Region/State
4. Region -> Country

**Example**:
```
Original: "123 Oak Street, Springfield, Illinois"
Level 1: "Oak Street area, Springfield, Illinois"
Level 2: "Springfield, Illinois"
Level 3: "Central Illinois"
Level 4: "Midwestern United States"
```

### 6. K-Anonymity Techniques

**Description**: Ensure each record is indistinguishable from at least k-1 other records.

**Application**:
- Age ranges instead of exact ages
- Salary bands instead of exact figures
- Generalized job titles

**Example** (k=5):
```
Original ages: 23, 24, 25, 27, 28, 31, 32, 33, 34, 35
Generalized: 20-29, 20-29, 20-29, 20-29, 20-29, 30-39, 30-39, 30-39, 30-39, 30-39
```

## Identifier Types and Recommended Techniques

| Identifier Type | Risk Level | Recommended Technique |
|-----------------|------------|----------------------|
| Full Name | High | Direct replacement with pseudonym |
| Email Address | High | Pattern redaction |
| Phone Number | High | Pattern redaction |
| Home Address | High | Full redaction or geographic generalization |
| SSN/National ID | Critical | Full redaction |
| Date of Birth | Medium | Date shifting or age range |
| Employer | Medium | Categorical replacement |
| Job Title | Low-Medium | Generalization |
| Medical Condition | High | Categorical (if needed) or redact |
| Financial Data | High | Range/band replacement |

## Compound Identifiers

**Warning**: Combinations of seemingly innocuous data can enable re-identification.

**Example of Quasi-Identifiers**:
- ZIP code + Birth date + Gender = 87% of US population uniquely identified
- Profession + City + Age range = Often uniquely identifying

**Mitigation**:
1. Apply k-anonymity across quasi-identifier combinations
2. Generalize multiple fields simultaneously
3. Consider suppression of outliers

## Document-Specific Considerations

### Legal Documents
- Preserve structure and clause references
- Maintain legal terminology while replacing names
- Consider redacting case numbers and court identifiers

### Medical Records
- HIPAA requires removal of 18 identifier types
- Preserve clinical utility where possible
- Date shifting preferred over date removal

### Financial Documents
- Redact account numbers completely
- Use ranges for monetary values if exact amounts not needed
- Remove routing numbers and bank identifiers

### Communications (Email/Chat)
- Redact headers including IP addresses and server names
- Replace email addresses in body text
- Consider timestamp implications

## Quality Assurance

### Pre-Redaction Checklist
- [ ] Identify all sensitive entity types
- [ ] Choose appropriate technique for each type
- [ ] Determine if cross-document consistency needed
- [ ] Plan for metadata handling

### Post-Redaction Verification
- [ ] Search for original sensitive terms
- [ ] Check for partial matches or variations
- [ ] Verify metadata removal
- [ ] Test for inferential disclosure (can redacted info be deduced?)
- [ ] Review for consistency in replacements
