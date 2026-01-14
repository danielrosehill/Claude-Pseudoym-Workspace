#!/usr/bin/env python3
"""
Text Redactor - Replace sensitive information in text files.

Supports:
- Direct replacement with aliases
- Pattern-based redaction (emails, phones, SSNs)
- Random identifier generation
- Consistent alias mapping
"""

import re
import json
import hashlib
import secrets
import string
from pathlib import Path
from datetime import datetime
from typing import Optional


class TextRedactor:
    """Text redaction with multiple strategies."""

    # Common patterns for sensitive information
    PATTERNS = {
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone_us': r'\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
        'phone_intl': r'\b\+?[1-9]\d{1,14}\b',
        'ssn': r'\b\d{3}[-\s]?\d{2}[-\s]?\d{4}\b',
        'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
        'ip_address': r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
        'date_mdy': r'\b(?:0?[1-9]|1[0-2])[/.-](?:0?[1-9]|[12]\d|3[01])[/.-](?:\d{2}|\d{4})\b',
        'date_dmy': r'\b(?:0?[1-9]|[12]\d|3[01])[/.-](?:0?[1-9]|1[0-2])[/.-](?:\d{2}|\d{4})\b',
    }

    def __init__(self, mapping_file: Optional[Path] = None):
        """Initialize redactor with optional existing mapping."""
        self.mapping = self._load_mapping(mapping_file) if mapping_file else self._empty_mapping()
        self.redaction_log = []
        self._random_counter = {}

    def _empty_mapping(self) -> dict:
        """Create empty mapping structure."""
        return {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "entities": []
        }

    def _load_mapping(self, path: Path) -> dict:
        """Load existing mapping from file."""
        if path.exists():
            with open(path, 'r') as f:
                return json.load(f)
        return self._empty_mapping()

    def save_mapping(self, path: Path):
        """Save current mapping to file."""
        self.mapping['updated'] = datetime.now().isoformat()
        with open(path, 'w') as f:
            json.dump(self.mapping, f, indent=2)

    def add_alias(self, original: str, alias: str, entity_type: str = "other",
                  variations: list = None, notes: str = ""):
        """Add an entity to the mapping."""
        entity = {
            "original": original,
            "alias": alias,
            "type": entity_type,
            "variations": variations or [],
            "notes": notes
        }
        self.mapping['entities'].append(entity)

    def _generate_random_id(self, prefix: str = "ID") -> str:
        """Generate a random identifier."""
        chars = string.ascii_uppercase + string.digits
        random_part = ''.join(secrets.choice(chars) for _ in range(8))
        return f"{prefix}-{random_part}"

    def _get_pattern_replacement(self, pattern_type: str, match_text: str,
                                 random_mode: bool = False) -> str:
        """Get replacement text for a pattern match."""
        if random_mode:
            # Generate unique ID for each match
            if pattern_type not in self._random_counter:
                self._random_counter[pattern_type] = 0
            self._random_counter[pattern_type] += 1
            return f"[{pattern_type.upper()}-{self._random_counter[pattern_type]:03d}]"
        else:
            return f"[{pattern_type.upper()}-REDACTED]"

    def redact_patterns(self, text: str, patterns: list = None,
                        random_mode: bool = False) -> str:
        """Redact text based on regex patterns."""
        if patterns is None:
            patterns = list(self.PATTERNS.keys())

        result = text
        for pattern_name in patterns:
            if pattern_name in self.PATTERNS:
                pattern = self.PATTERNS[pattern_name]

                def replace_func(match):
                    original = match.group(0)
                    replacement = self._get_pattern_replacement(pattern_name, original, random_mode)
                    self.redaction_log.append({
                        "type": "pattern",
                        "pattern": pattern_name,
                        "original": original,
                        "replacement": replacement
                    })
                    return replacement

                result = re.sub(pattern, replace_func, result)

        return result

    def redact_entities(self, text: str, case_sensitive: bool = False) -> str:
        """Redact text based on entity mapping."""
        result = text
        flags = 0 if case_sensitive else re.IGNORECASE

        for entity in self.mapping['entities']:
            # Redact original term
            terms_to_replace = [entity['original']] + entity.get('variations', [])

            for term in terms_to_replace:
                if not term:
                    continue
                # Use word boundaries to avoid partial matches
                pattern = r'\b' + re.escape(term) + r'\b'

                def make_replacer(alias, orig_term):
                    def replacer(match):
                        self.redaction_log.append({
                            "type": "entity",
                            "original": match.group(0),
                            "replacement": alias,
                            "mapped_from": orig_term
                        })
                        return alias
                    return replacer

                result = re.sub(pattern, make_replacer(entity['alias'], term),
                               result, flags=flags)

        return result

    def redact_with_random_ids(self, text: str, entities: list,
                               entity_type: str = "ENTITY") -> tuple[str, dict]:
        """Redact entities with random IDs (per-document unique)."""
        result = text
        document_mapping = {}

        for entity in entities:
            if entity not in document_mapping:
                random_id = self._generate_random_id(entity_type)
                document_mapping[entity] = random_id

            pattern = r'\b' + re.escape(entity) + r'\b'
            result = re.sub(pattern, document_mapping[entity], result, flags=re.IGNORECASE)

            self.redaction_log.append({
                "type": "random",
                "original": entity,
                "replacement": document_mapping[entity]
            })

        return result, document_mapping

    def analyze_text(self, text: str) -> dict:
        """Analyze text for potentially sensitive information."""
        findings = {
            "patterns": {},
            "statistics": {
                "total_matches": 0
            }
        }

        for pattern_name, pattern in self.PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                findings["patterns"][pattern_name] = {
                    "count": len(matches),
                    "samples": list(set(matches))[:5]  # Show up to 5 unique samples
                }
                findings["statistics"]["total_matches"] += len(matches)

        return findings

    def get_redaction_report(self) -> dict:
        """Get summary of redactions performed."""
        report = {
            "total_redactions": len(self.redaction_log),
            "by_type": {},
            "details": self.redaction_log
        }

        for entry in self.redaction_log:
            entry_type = entry.get("type", "unknown")
            if entry_type not in report["by_type"]:
                report["by_type"][entry_type] = 0
            report["by_type"][entry_type] += 1

        return report

    def clear_log(self):
        """Clear the redaction log for a new document."""
        self.redaction_log = []
        self._random_counter = {}


def process_file(input_path: Path, output_path: Path, redactor: TextRedactor,
                 patterns: list = None, random_mode: bool = False) -> dict:
    """Process a single text file."""
    with open(input_path, 'r', encoding='utf-8') as f:
        content = f.read()

    redactor.clear_log()

    # Apply entity redaction first
    result = redactor.redact_entities(content)

    # Then pattern redaction
    if patterns:
        result = redactor.redact_patterns(result, patterns, random_mode)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    return redactor.get_redaction_report()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Redact sensitive information from text files")
    parser.add_argument("input", help="Input file path")
    parser.add_argument("output", help="Output file path")
    parser.add_argument("--mapping", "-m", help="Path to alias mapping JSON file")
    parser.add_argument("--patterns", "-p", nargs="+",
                        choices=list(TextRedactor.PATTERNS.keys()),
                        help="Patterns to redact")
    parser.add_argument("--random", "-r", action="store_true",
                        help="Use random IDs for pattern matches")
    parser.add_argument("--analyze", "-a", action="store_true",
                        help="Analyze file without redacting")

    args = parser.parse_args()

    mapping_path = Path(args.mapping) if args.mapping else None
    redactor = TextRedactor(mapping_path)

    if args.analyze:
        with open(args.input, 'r') as f:
            content = f.read()
        findings = redactor.analyze_text(content)
        print(json.dumps(findings, indent=2))
    else:
        report = process_file(
            Path(args.input),
            Path(args.output),
            redactor,
            args.patterns,
            args.random
        )
        print(f"Redaction complete. {report['total_redactions']} replacements made.")
        print(json.dumps(report, indent=2))
