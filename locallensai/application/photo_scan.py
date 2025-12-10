from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Set

from locallensai.config import SUPPORTED_IMAGE_EXTENSIONS
from locallensai.domain.models import Photo
from locallensai.infrastructure.gateways.filesystem import FileSystemGateway
from .metadata_extraction import MetadataExtractionService


@dataclass
class ScanReport:
    scanned_files: int = 0
    skipped_files: int = 0
    valid_photos: int = 0


class PhotoScanService:
    """Scans directories for images and extracts metadata."""

    def __init__(
        self,
        filesystem: FileSystemGateway,
        metadata_service: MetadataExtractionService,
        supported_extensions: Optional[Iterable[str]] = None,
    ) -> None:
        self._filesystem = filesystem
        self._metadata_service = metadata_service
        extensions = supported_extensions or SUPPORTED_IMAGE_EXTENSIONS
        self._extensions: Set[str] = {ext.lower() for ext in extensions}

    def scan(self, root_path: Path) -> tuple[List[Photo], ScanReport]:
        photos: List[Photo] = []
        report = ScanReport()

        for file_path in self._filesystem.iterate_files(root_path, self._extensions):
            report.scanned_files += 1
            photo = self._metadata_service.extract_photo(file_path, original_folder=file_path.parent.name)
            if photo is None:
                report.skipped_files += 1
                continue
            photos.append(photo)
            report.valid_photos += 1

        photos.sort()
        return photos, report
