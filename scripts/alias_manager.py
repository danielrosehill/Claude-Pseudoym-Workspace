#!/usr/bin/env python3
"""
Alias Manager - Manage persistent pseudonym mappings.

Features:
- Create and manage alias mappings
- Import/export mappings
- Validate mapping consistency
- Generate reports
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional


class AliasManager:
    """Manage alias mappings for redaction."""

    def __init__(self, mapping_file: Optional[Path] = None):
        """Initialize with optional existing mapping file."""
        self.mapping_file = mapping_file
        if mapping_file and mapping_file.exists():
            self.mapping = self._load(mapping_file)
        else:
            self.mapping = self._empty_mapping()

    def _empty_mapping(self) -> dict:
        """Create empty mapping structure."""
        return {
            "version": "1.0",
            "created": datetime.now().isoformat(),
            "updated": datetime.now().isoformat(),
            "entities": []
        }

    def _load(self, path: Path) -> dict:
        """Load mapping from file."""
        with open(path, 'r') as f:
            return json.load(f)

    def save(self, path: Optional[Path] = None):
        """Save mapping to file."""
        path = path or self.mapping_file
        if not path:
            raise ValueError("No path specified and no default mapping file set")

        self.mapping['updated'] = datetime.now().isoformat()
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w') as f:
            json.dump(self.mapping, f, indent=2)

    def add_entity(self, original: str, alias: str, entity_type: str = "other",
                   variations: list = None, notes: str = "") -> bool:
        """Add a new entity to the mapping."""
        # Check for duplicates
        for entity in self.mapping['entities']:
            if entity['original'].lower() == original.lower():
                return False  # Already exists
            if entity['alias'].lower() == alias.lower():
                return False  # Alias already in use

        entity = {
            "original": original,
            "alias": alias,
            "type": entity_type,
            "variations": variations or [],
            "notes": notes,
            "added": datetime.now().isoformat()
        }

        self.mapping['entities'].append(entity)
        return True

    def remove_entity(self, original: str) -> bool:
        """Remove an entity from the mapping."""
        for i, entity in enumerate(self.mapping['entities']):
            if entity['original'].lower() == original.lower():
                del self.mapping['entities'][i]
                return True
        return False

    def get_entity(self, original: str) -> Optional[dict]:
        """Get entity by original name."""
        for entity in self.mapping['entities']:
            if entity['original'].lower() == original.lower():
                return entity
            # Also check variations
            for var in entity.get('variations', []):
                if var.lower() == original.lower():
                    return entity
        return None

    def get_alias(self, original: str) -> Optional[str]:
        """Get alias for an original term."""
        entity = self.get_entity(original)
        return entity['alias'] if entity else None

    def update_entity(self, original: str, **kwargs) -> bool:
        """Update an existing entity."""
        entity = self.get_entity(original)
        if not entity:
            return False

        allowed_fields = ['alias', 'type', 'variations', 'notes']
        for field, value in kwargs.items():
            if field in allowed_fields:
                entity[field] = value

        return True

    def add_variation(self, original: str, variation: str) -> bool:
        """Add a variation to an existing entity."""
        entity = self.get_entity(original)
        if not entity:
            return False

        if 'variations' not in entity:
            entity['variations'] = []

        if variation not in entity['variations']:
            entity['variations'].append(variation)

        return True

    def list_entities(self, entity_type: str = None) -> list:
        """List all entities, optionally filtered by type."""
        if entity_type:
            return [e for e in self.mapping['entities'] if e.get('type') == entity_type]
        return self.mapping['entities']

    def get_statistics(self) -> dict:
        """Get statistics about the mapping."""
        stats = {
            "total": len(self.mapping['entities']),
            "by_type": {},
            "created": self.mapping.get('created'),
            "updated": self.mapping.get('updated')
        }

        for entity in self.mapping['entities']:
            etype = entity.get('type', 'other')
            stats['by_type'][etype] = stats['by_type'].get(etype, 0) + 1

        return stats

    def export_csv(self, path: Path):
        """Export mapping to CSV format."""
        import csv

        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Original', 'Alias', 'Type', 'Variations', 'Notes'])

            for entity in self.mapping['entities']:
                writer.writerow([
                    entity['original'],
                    entity['alias'],
                    entity.get('type', ''),
                    '; '.join(entity.get('variations', [])),
                    entity.get('notes', '')
                ])

    def import_csv(self, path: Path, overwrite: bool = False) -> dict:
        """Import mapping from CSV format."""
        import csv

        results = {"added": 0, "skipped": 0, "errors": []}

        with open(path, 'r') as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    variations = [v.strip() for v in row.get('Variations', '').split(';') if v.strip()]

                    if overwrite:
                        # Remove existing if present
                        self.remove_entity(row['Original'])

                    success = self.add_entity(
                        original=row['Original'],
                        alias=row['Alias'],
                        entity_type=row.get('Type', 'other'),
                        variations=variations,
                        notes=row.get('Notes', '')
                    )

                    if success:
                        results["added"] += 1
                    else:
                        results["skipped"] += 1
                except Exception as e:
                    results["errors"].append(str(e))

        return results

    def validate(self) -> dict:
        """Validate the mapping for consistency."""
        issues = []

        # Check for duplicate originals
        originals = [e['original'].lower() for e in self.mapping['entities']]
        duplicates = set([x for x in originals if originals.count(x) > 1])
        if duplicates:
            issues.append(f"Duplicate originals: {duplicates}")

        # Check for duplicate aliases
        aliases = [e['alias'].lower() for e in self.mapping['entities']]
        dup_aliases = set([x for x in aliases if aliases.count(x) > 1])
        if dup_aliases:
            issues.append(f"Duplicate aliases: {dup_aliases}")

        # Check for empty required fields
        for i, entity in enumerate(self.mapping['entities']):
            if not entity.get('original'):
                issues.append(f"Entity {i}: missing original")
            if not entity.get('alias'):
                issues.append(f"Entity {i}: missing alias")

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

    def merge(self, other_mapping: dict, conflict_strategy: str = "skip") -> dict:
        """Merge another mapping into this one."""
        results = {"added": 0, "skipped": 0, "overwritten": 0}

        for entity in other_mapping.get('entities', []):
            existing = self.get_entity(entity['original'])

            if existing:
                if conflict_strategy == "overwrite":
                    self.remove_entity(entity['original'])
                    self.add_entity(
                        original=entity['original'],
                        alias=entity['alias'],
                        entity_type=entity.get('type', 'other'),
                        variations=entity.get('variations', []),
                        notes=entity.get('notes', '')
                    )
                    results["overwritten"] += 1
                else:  # skip
                    results["skipped"] += 1
            else:
                self.add_entity(
                    original=entity['original'],
                    alias=entity['alias'],
                    entity_type=entity.get('type', 'other'),
                    variations=entity.get('variations', []),
                    notes=entity.get('notes', '')
                )
                results["added"] += 1

        return results


def print_table(entities: list):
    """Print entities in table format."""
    if not entities:
        print("No entities in mapping.")
        return

    # Calculate column widths
    orig_width = max(len(e['original']) for e in entities)
    alias_width = max(len(e['alias']) for e in entities)
    type_width = max(len(e.get('type', 'other')) for e in entities)

    # Header
    print(f"{'Original':<{orig_width}} | {'Alias':<{alias_width}} | {'Type':<{type_width}} | Variations")
    print("-" * (orig_width + alias_width + type_width + 20))

    # Rows
    for e in entities:
        vars_str = ', '.join(e.get('variations', []))[:30]
        print(f"{e['original']:<{orig_width}} | {e['alias']:<{alias_width}} | {e.get('type', 'other'):<{type_width}} | {vars_str}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Manage alias mappings")
    parser.add_argument("mapping_file", help="Path to mapping JSON file")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List all entities")
    list_parser.add_argument("--type", "-t", help="Filter by type")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add new entity")
    add_parser.add_argument("original", help="Original term")
    add_parser.add_argument("alias", help="Alias to use")
    add_parser.add_argument("--type", "-t", default="other", help="Entity type")
    add_parser.add_argument("--variations", "-v", nargs="+", help="Variations")
    add_parser.add_argument("--notes", "-n", default="", help="Notes")

    # Remove command
    remove_parser = subparsers.add_parser("remove", help="Remove entity")
    remove_parser.add_argument("original", help="Original term to remove")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export to CSV")
    export_parser.add_argument("output", help="Output CSV file")

    # Import command
    import_parser = subparsers.add_parser("import", help="Import from CSV")
    import_parser.add_argument("input", help="Input CSV file")
    import_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing")

    # Stats command
    subparsers.add_parser("stats", help="Show statistics")

    # Validate command
    subparsers.add_parser("validate", help="Validate mapping")

    args = parser.parse_args()

    mapping_path = Path(args.mapping_file)
    manager = AliasManager(mapping_path if mapping_path.exists() else None)

    if args.command == "list":
        entities = manager.list_entities(args.type)
        print_table(entities)

    elif args.command == "add":
        success = manager.add_entity(
            args.original, args.alias, args.type,
            args.variations, args.notes
        )
        if success:
            manager.save(mapping_path)
            print(f"Added: {args.original} -> {args.alias}")
        else:
            print("Failed to add (duplicate original or alias)")

    elif args.command == "remove":
        success = manager.remove_entity(args.original)
        if success:
            manager.save(mapping_path)
            print(f"Removed: {args.original}")
        else:
            print("Entity not found")

    elif args.command == "export":
        manager.export_csv(Path(args.output))
        print(f"Exported to {args.output}")

    elif args.command == "import":
        results = manager.import_csv(Path(args.input), args.overwrite)
        manager.save(mapping_path)
        print(f"Import results: {results}")

    elif args.command == "stats":
        stats = manager.get_statistics()
        print(json.dumps(stats, indent=2))

    elif args.command == "validate":
        result = manager.validate()
        if result["valid"]:
            print("Mapping is valid.")
        else:
            print("Validation issues:")
            for issue in result["issues"]:
                print(f"  - {issue}")

    else:
        parser.print_help()
