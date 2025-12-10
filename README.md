# LocalLensAI

LocalLensAI is a local-only, AI-ready photo organizer. Stage 1 focuses on a clean architecture foundation, photo scanning, and EXIF/metadata extraction.

## Features
- Domain model for photos and events.
- Application services for scanning directories and extracting metadata.
- Infrastructure adapters for filesystem access and EXIF handling via Pillow.
- Minimal CLI stub to scan a directory and print a summary.
- Basic tests for image validation and datetime normalization.

## Usage
```
python -m locallensai.presentation.main /path/to/photos
```

## Development
Install dependencies:
```
pip install -r requirements.txt
```
Run tests:
```
pytest
```
