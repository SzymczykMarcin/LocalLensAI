from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from locallensai.application.metadata_extraction import MetadataExtractionService
from locallensai.application.photo_scan import PhotoScanService
from locallensai.domain.models import Photo
from locallensai.infrastructure.exif import ExifMetadataAdapter
from locallensai.infrastructure.gateways import LocalFileSystemGateway


def summarize_photos(photos: List[Photo]) -> str:
    preview = photos[:5]
    summary_lines = [f"Total photos: {len(photos)}", "Sample:"]
    for photo in preview:
        timestamp = photo.capture_datetime.isoformat() if photo.capture_datetime else "Unknown"
        gps = photo.gps_coordinates or "N/A"
        summary_lines.append(f"- {photo.path} | {timestamp} | GPS: {gps}")
    return "\n".join(summary_lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="LocalLensAI photo organizer - Stage 1")
    parser.add_argument("root", type=Path, help="Root directory to scan for images")
    args = parser.parse_args()

    filesystem = LocalFileSystemGateway()
    exif_adapter = ExifMetadataAdapter()
    metadata_service = MetadataExtractionService(filesystem=filesystem, exif_adapter=exif_adapter)
    scanner = PhotoScanService(filesystem=filesystem, metadata_service=metadata_service)

    photos, report = scanner.scan(args.root)

    print(f"Scanned files: {report.scanned_files}")
    print(f"Skipped files: {report.skipped_files}")
    print(f"Valid photos: {report.valid_photos}")
    print(summarize_photos(photos))


if __name__ == "__main__":
    main()
