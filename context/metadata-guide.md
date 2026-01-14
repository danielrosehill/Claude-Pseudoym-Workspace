# Metadata Scrubbing Guide

## Overview

Metadata can reveal as much about a document's origin as its content. This guide covers identifying and removing metadata from various file types.

## Why Metadata Matters

### Real-World Exposure Examples

1. **EXIF GPS Data**: Photos revealing exact location of safe houses
2. **Document Author**: Microsoft Office "Author" field exposing source identity
3. **Revision History**: Track changes showing original text before redaction
4. **Printer Tracking Dots**: Yellow dots identifying specific printer and timestamp
5. **PDF Metadata**: Creation software, author, and modification dates

## Metadata by File Type

### Images (JPEG, PNG, TIFF)

**Common Metadata Fields**:
- GPS coordinates (latitude/longitude)
- Camera make/model
- Date/time taken
- Software used to edit
- Thumbnail images (may contain un-edited version)
- Copyright and author information
- Unique image IDs

**Removal Tools**:
```bash
# ExifTool - comprehensive metadata removal
exiftool -all= image.jpg

# Remove all metadata but keep orientation
exiftool -all= -tagsfromfile @ -orientation image.jpg

# Batch process directory
exiftool -all= -r /path/to/directory/
```

### PDF Documents

**Metadata Locations**:
- Document properties (Title, Author, Subject, Keywords)
- XMP metadata stream
- Embedded fonts with identifying information
- Creation/modification dates
- PDF producer software
- Embedded files and attachments
- JavaScript
- Form field data
- Comments and annotations

**Removal Tools**:
```bash
# qpdf - linearize and remove metadata
qpdf --linearize --replace-input document.pdf

# Using exiftool
exiftool -all:all= document.pdf

# Using pdftk
pdftk input.pdf dump_data | \
  sed -e 's/InfoValue:.*/InfoValue:/' | \
  pdftk input.pdf update_info - output clean.pdf
```

### Microsoft Office Documents (.docx, .xlsx, .pptx)

**Metadata Locations**:
- Document properties (core.xml)
- Author and last modified by
- Revision number
- Total editing time
- Company name
- Comments
- Track changes / revision history
- Hidden rows/columns (Excel)
- Speaker notes (PowerPoint)
- Embedded objects

**Removal Method**:
```bash
# Using LibreOffice
libreoffice --headless --convert-to pdf --outdir output/ document.docx

# Manual: Unzip, edit XML, rezip
unzip document.docx -d temp/
# Edit temp/docProps/core.xml and temp/docProps/app.xml
cd temp && zip -r ../clean.docx *
```

### Audio Files (MP3, WAV, FLAC)

**Metadata Fields**:
- ID3 tags (artist, album, etc.)
- Recording software
- Recording device
- Timestamps
- Embedded images

**Removal Tools**:
```bash
# FFmpeg - strip all metadata
ffmpeg -i input.mp3 -map_metadata -1 -c:a copy output.mp3

# For complete re-encoding (removes hidden data)
ffmpeg -i input.mp3 -map_metadata -1 output.mp3
```

### Video Files (MP4, MKV, AVI)

**Metadata Fields**:
- Recording device/software
- GPS data
- Creation date
- Encoder information
- Chapter markers
- Embedded subtitles with identifying info

**Removal Tools**:
```bash
# FFmpeg - strip metadata
ffmpeg -i input.mp4 -map_metadata -1 -c:v copy -c:a copy output.mp4

# Also remove chapter data
ffmpeg -i input.mp4 -map_metadata -1 -map_chapters -1 -c copy output.mp4
```

## Deep Cleaning Considerations

### Hidden Data That Survives Basic Scrubbing

1. **Steganography**: Data hidden within image pixels
2. **Printer Tracking Dots**: Microscopic yellow dots on printed/scanned documents
3. **Font Subsetting**: Embedded font subsets can be fingerprinted
4. **File System Metadata**: Creation/access times, alternate data streams
5. **Slack Space**: Residual data in file slack space

### Recommended Deep Clean Process

1. **Convert to intermediate format**
   ```bash
   # Images: Re-encode through clean pipeline
   convert input.jpg -strip -quality 85 output.jpg

   # Documents: Print to PDF then re-render
   ```

2. **Verify with multiple tools**
   ```bash
   exiftool -all file.jpg
   pdfinfo document.pdf
   strings file.pdf | grep -i author
   ```

3. **Check file size anomalies** - Unexpected large size may indicate hidden data

## Batch Processing Scripts

### Clean All Images in Directory
```bash
#!/bin/bash
find /path/to/input -type f \( -iname "*.jpg" -o -iname "*.png" \) | while read f; do
    exiftool -all= -overwrite_original "$f"
done
```

### Clean All PDFs in Directory
```bash
#!/bin/bash
find /path/to/input -type f -iname "*.pdf" | while read f; do
    qpdf --linearize "$f" "${f%.pdf}_clean.pdf"
    exiftool -all:all= -overwrite_original "${f%.pdf}_clean.pdf"
done
```

## Verification Checklist

- [ ] Run `exiftool -all <file>` and verify empty/minimal output
- [ ] Check document properties in native application
- [ ] Search file with `strings` command for sensitive terms
- [ ] Verify file size is reasonable (no hidden attachments)
- [ ] Test with online metadata viewers for second opinion
- [ ] For images, check thumbnail doesn't contain original

## Tools Reference

| Tool | Platform | Best For |
|------|----------|----------|
| ExifTool | Cross-platform | Images, PDFs, documents |
| qpdf | Cross-platform | PDF linearization and cleaning |
| mat2 | Linux | Multiple formats, privacy-focused |
| FFmpeg | Cross-platform | Audio/video |
| ImageMagick | Cross-platform | Image conversion and cleaning |
| pdftk | Cross-platform | PDF manipulation |

## Installation (Ubuntu/Debian)

```bash
sudo apt install exiftool qpdf mat2 ffmpeg imagemagick pdftk-java
```
