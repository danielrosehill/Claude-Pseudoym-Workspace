# /scrub-metadata - Metadata Removal

Remove all metadata from files to prevent identification through document properties.

## Workflow

1. **Inventory files**: List all files in `/input/` or `/output/`
2. **Identify file types**: Determine appropriate cleaning method for each
3. **Check for tools**: Verify required tools are available (exiftool, qpdf, ffmpeg)
4. **Execute cleaning**: Remove metadata using appropriate tool for each file type
5. **Verify removal**: Confirm metadata has been stripped
6. **Report results**: Show what was removed from each file

## Supported File Types

| Type | Extensions | Tool Used |
|------|------------|-----------|
| Images | .jpg, .jpeg, .png, .gif, .tiff | exiftool |
| PDF | .pdf | qpdf + exiftool |
| Office | .docx, .xlsx, .pptx | libreoffice conversion |
| Audio | .mp3, .wav, .flac | ffmpeg |
| Video | .mp4, .mkv, .avi | ffmpeg |

## Commands Used

```bash
# Images
exiftool -all= -overwrite_original <file>

# PDFs
qpdf --linearize <input> <output>
exiftool -all:all= <file>

# Audio/Video
ffmpeg -i <input> -map_metadata -1 -c copy <output>
```

## Output

- Cleaned files replace originals (or create new files in /output/)
- Report showing:
  - What metadata was present
  - What was removed
  - Verification of clean state

## Example Invocation

User: `/scrub-metadata`

Claude: I'll check the files and remove all metadata.

**Files found:**
- photo_evidence.jpg
- document.pdf

**Processing photo_evidence.jpg...**
- Removed: Camera make/model, GPS coordinates, Date taken, Software
- Verified clean: Yes

**Processing document.pdf...**
- Removed: Author, Creator, Creation date, Modification date, Producer
- Verified clean: Yes

All files have been scrubbed of metadata.

## Options

- Process `/input/` directory (default)
- Process `/output/` directory (for post-redaction cleanup)
- Process specific file
- Preserve certain metadata (e.g., keep orientation for images)
