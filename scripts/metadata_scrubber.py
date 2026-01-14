#!/usr/bin/env python3
"""
Metadata Scrubber - Remove metadata from various file types.

Supports:
- Images (JPEG, PNG, TIFF, GIF)
- PDFs
- Office documents (DOCX, XLSX, PPTX)
- Audio (MP3, WAV, FLAC)
- Video (MP4, MKV, AVI)

Requires external tools:
- exiftool (for images and general metadata)
- qpdf (for PDF linearization)
- ffmpeg (for audio/video)
"""

import subprocess
import shutil
import json
from pathlib import Path
from typing import Optional
import tempfile


class MetadataScrubber:
    """Remove metadata from files."""

    # File type mappings
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.tiff', '.tif', '.bmp', '.webp'}
    PDF_EXTENSIONS = {'.pdf'}
    OFFICE_EXTENSIONS = {'.docx', '.xlsx', '.pptx', '.odt', '.ods', '.odp'}
    AUDIO_EXTENSIONS = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'}
    VIDEO_EXTENSIONS = {'.mp4', '.mkv', '.avi', '.mov', '.webm', '.wmv'}

    def __init__(self):
        """Initialize scrubber and check for required tools."""
        self.available_tools = self._check_tools()

    def _check_tools(self) -> dict:
        """Check which tools are available."""
        tools = {
            'exiftool': shutil.which('exiftool') is not None,
            'qpdf': shutil.which('qpdf') is not None,
            'ffmpeg': shutil.which('ffmpeg') is not None,
            'libreoffice': shutil.which('libreoffice') is not None,
        }
        return tools

    def _run_command(self, cmd: list, check: bool = True) -> subprocess.CompletedProcess:
        """Run a shell command."""
        return subprocess.run(cmd, capture_output=True, text=True, check=check)

    def get_metadata(self, file_path: Path) -> dict:
        """Extract metadata from a file using exiftool."""
        if not self.available_tools['exiftool']:
            return {"error": "exiftool not available"}

        try:
            result = self._run_command(['exiftool', '-json', str(file_path)])
            metadata = json.loads(result.stdout)
            return metadata[0] if metadata else {}
        except subprocess.CalledProcessError as e:
            return {"error": str(e)}
        except json.JSONDecodeError:
            return {"error": "Failed to parse metadata"}

    def scrub_image(self, input_path: Path, output_path: Optional[Path] = None,
                    preserve_orientation: bool = True) -> dict:
        """Remove metadata from image files."""
        if not self.available_tools['exiftool']:
            return {"success": False, "error": "exiftool not available"}

        output_path = output_path or input_path

        try:
            if preserve_orientation:
                # Remove all metadata but preserve orientation
                cmd = ['exiftool', '-all=', '-tagsfromfile', '@',
                       '-orientation', '-overwrite_original', str(input_path)]
            else:
                cmd = ['exiftool', '-all=', '-overwrite_original', str(input_path)]

            self._run_command(cmd)

            # Copy to output if different
            if output_path != input_path:
                shutil.copy2(input_path, output_path)

            return {"success": True, "output": str(output_path)}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": str(e)}

    def scrub_pdf(self, input_path: Path, output_path: Optional[Path] = None) -> dict:
        """Remove metadata from PDF files."""
        output_path = output_path or input_path.with_suffix('.clean.pdf')

        results = {"success": True, "steps": []}

        # Step 1: Linearize with qpdf if available
        if self.available_tools['qpdf']:
            try:
                with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp:
                    tmp_path = Path(tmp.name)

                cmd = ['qpdf', '--linearize', str(input_path), str(tmp_path)]
                self._run_command(cmd)
                results["steps"].append("qpdf linearization")

                # Use linearized version for next step
                working_path = tmp_path
            except subprocess.CalledProcessError as e:
                results["steps"].append(f"qpdf failed: {e}")
                working_path = input_path
        else:
            working_path = input_path
            results["steps"].append("qpdf not available, skipping linearization")

        # Step 2: Remove metadata with exiftool
        if self.available_tools['exiftool']:
            try:
                # Copy to output first
                shutil.copy2(working_path, output_path)

                cmd = ['exiftool', '-all:all=', '-overwrite_original', str(output_path)]
                self._run_command(cmd)
                results["steps"].append("exiftool metadata removal")
            except subprocess.CalledProcessError as e:
                results["success"] = False
                results["steps"].append(f"exiftool failed: {e}")
        else:
            results["success"] = False
            results["steps"].append("exiftool not available")

        # Clean up temp file
        if 'tmp_path' in locals() and tmp_path.exists():
            tmp_path.unlink()

        results["output"] = str(output_path)
        return results

    def scrub_audio_video(self, input_path: Path, output_path: Optional[Path] = None,
                          reencode: bool = False) -> dict:
        """Remove metadata from audio/video files."""
        if not self.available_tools['ffmpeg']:
            return {"success": False, "error": "ffmpeg not available"}

        suffix = input_path.suffix
        output_path = output_path or input_path.with_name(f"{input_path.stem}_clean{suffix}")

        try:
            if reencode:
                # Full re-encode (slower but more thorough)
                cmd = ['ffmpeg', '-i', str(input_path), '-map_metadata', '-1',
                       '-y', str(output_path)]
            else:
                # Copy streams (faster, preserves quality)
                cmd = ['ffmpeg', '-i', str(input_path), '-map_metadata', '-1',
                       '-c', 'copy', '-y', str(output_path)]

            self._run_command(cmd)
            return {"success": True, "output": str(output_path)}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": str(e.stderr)}

    def scrub_office(self, input_path: Path, output_path: Optional[Path] = None) -> dict:
        """Remove metadata from Office documents by converting to PDF and back."""
        # Note: This is a destructive conversion. For true metadata removal
        # while preserving format, use LibreOffice's built-in tools or
        # programmatic XML manipulation.

        if not self.available_tools['libreoffice']:
            return {"success": False, "error": "libreoffice not available",
                    "note": "Consider using File > Properties > Reset in LibreOffice"}

        output_path = output_path or input_path.with_suffix('.pdf')

        try:
            # Convert to PDF (removes most metadata)
            cmd = ['libreoffice', '--headless', '--convert-to', 'pdf',
                   '--outdir', str(output_path.parent), str(input_path)]
            self._run_command(cmd)

            return {"success": True, "output": str(output_path),
                    "note": "Converted to PDF to remove metadata"}
        except subprocess.CalledProcessError as e:
            return {"success": False, "error": str(e)}

    def scrub_file(self, input_path: Path, output_path: Optional[Path] = None) -> dict:
        """Auto-detect file type and scrub metadata."""
        input_path = Path(input_path)
        ext = input_path.suffix.lower()

        if ext in self.IMAGE_EXTENSIONS:
            return self.scrub_image(input_path, output_path)
        elif ext in self.PDF_EXTENSIONS:
            return self.scrub_pdf(input_path, output_path)
        elif ext in self.AUDIO_EXTENSIONS or ext in self.VIDEO_EXTENSIONS:
            return self.scrub_audio_video(input_path, output_path)
        elif ext in self.OFFICE_EXTENSIONS:
            return self.scrub_office(input_path, output_path)
        else:
            return {"success": False, "error": f"Unsupported file type: {ext}"}

    def verify_clean(self, file_path: Path) -> dict:
        """Verify that a file has been cleaned of metadata."""
        metadata = self.get_metadata(file_path)

        # Fields that indicate remaining metadata
        sensitive_fields = [
            'Author', 'Creator', 'Producer', 'GPSLatitude', 'GPSLongitude',
            'Make', 'Model', 'Software', 'Artist', 'Copyright', 'Comment',
            'XPAuthor', 'XPComment', 'LastModifiedBy', 'Company'
        ]

        found_sensitive = []
        for field in sensitive_fields:
            if field in metadata and metadata[field]:
                found_sensitive.append({field: metadata[field]})

        return {
            "clean": len(found_sensitive) == 0,
            "remaining_sensitive": found_sensitive,
            "all_metadata": metadata
        }


def process_directory(input_dir: Path, output_dir: Path, scrubber: MetadataScrubber) -> list:
    """Process all supported files in a directory."""
    results = []

    supported_extensions = (
        scrubber.IMAGE_EXTENSIONS | scrubber.PDF_EXTENSIONS |
        scrubber.AUDIO_EXTENSIONS | scrubber.VIDEO_EXTENSIONS |
        scrubber.OFFICE_EXTENSIONS
    )

    for file_path in input_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in supported_extensions:
            output_path = output_dir / file_path.name
            result = scrubber.scrub_file(file_path, output_path)
            result["input"] = str(file_path)
            results.append(result)

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Remove metadata from files")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("--output", "-o", help="Output file or directory")
    parser.add_argument("--verify", "-v", action="store_true",
                        help="Verify file is clean instead of scrubbing")
    parser.add_argument("--show-metadata", "-m", action="store_true",
                        help="Show current metadata")
    parser.add_argument("--check-tools", "-c", action="store_true",
                        help="Check available tools")

    args = parser.parse_args()

    scrubber = MetadataScrubber()

    if args.check_tools:
        print("Available tools:")
        for tool, available in scrubber.available_tools.items():
            status = "OK" if available else "NOT FOUND"
            print(f"  {tool}: {status}")
        exit(0)

    input_path = Path(args.input)

    if args.show_metadata:
        metadata = scrubber.get_metadata(input_path)
        print(json.dumps(metadata, indent=2))
    elif args.verify:
        result = scrubber.verify_clean(input_path)
        if result["clean"]:
            print("File is clean of sensitive metadata.")
        else:
            print("Sensitive metadata found:")
            print(json.dumps(result["remaining_sensitive"], indent=2))
    else:
        if input_path.is_dir():
            output_dir = Path(args.output) if args.output else input_path / "cleaned"
            output_dir.mkdir(exist_ok=True)
            results = process_directory(input_path, output_dir, scrubber)
            for r in results:
                status = "OK" if r.get("success") else "FAILED"
                print(f"{r['input']}: {status}")
        else:
            output_path = Path(args.output) if args.output else None
            result = scrubber.scrub_file(input_path, output_path)
            print(json.dumps(result, indent=2))
