from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

from locallensai.domain.models import Photo
from locallensai.infrastructure.exif.adapter import ExifMetadataAdapter
from locallensai.infrastructure.gateways.filesystem import FileSystemGateway


class MetadataExtractionService:
    """Extracts metadata and builds photo entities."""

    def __init__(self, filesystem: FileSystemGateway, exif_adapter: ExifMetadataAdapter) -> None:
        self._filesystem = filesystem
        self._exif_adapter = exif_adapter

    def extract_photo(self, file_path: Path, original_folder: Optional[str] = None) -> Optional[Photo]:
        """Extract metadata from a file and return a populated Photo instance."""
        if not self._exif_adapter.is_image_valid(file_path):
            return None

        checksum = self._filesystem.compute_checksum(file_path)
        exif_payload = self._exif_adapter.extract_metadata(file_path)

        capture_datetime = self.normalize_datetime(exif_payload.get("datetime"))
        gps_coordinates = exif_payload.get("gps")

        photo = Photo(path=file_path, checksum=checksum, capture_datetime=capture_datetime, gps_coordinates=gps_coordinates)
        photo.add_exif_data(exif_payload.get("raw", {}))
        photo.original_folder = original_folder
        return photo

    @staticmethod
    def normalize_datetime(value: Optional[object]) -> Optional[datetime]:
        """Normalize EXIF date strings or datetime objects into datetime instances."""
        if value is None:
            return None

        if isinstance(value, datetime):
            return value

        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value)

        if isinstance(value, str):
            candidates: Iterable[str] = (
                "%Y:%m:%d %H:%M:%S",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%Y:%m:%d %H:%M:%S%z",
                "%Y-%m-%d %H:%M:%S%z",
                "%Y-%m-%dT%H:%M:%S%z",
            )
            for fmt in candidates:
                try:
                    return datetime.strptime(value, fmt)
                except ValueError:
                    continue
        return None
