from datetime import datetime
from pathlib import Path
from typing import Dict, Generator, Iterable

from locallensai.application.metadata_extraction import MetadataExtractionService
from locallensai.domain.models import Photo
from locallensai.infrastructure.gateways.filesystem import FileSystemGateway


class DummyFileSystemGateway(FileSystemGateway):
    def iterate_files(self, root_path: Path, extensions: Iterable[str]) -> Generator[Path, None, None]:
        yield from ()

    def compute_checksum(self, file_path: Path) -> str:
        return "checksum"


class DummyExifAdapter:
    def __init__(self, datetime_value: str) -> None:
        self.datetime_value = datetime_value

    def is_image_valid(self, file_path: Path) -> bool:
        return True

    def extract_metadata(self, file_path: Path) -> Dict[str, object]:
        return {"datetime": self.datetime_value, "gps": None, "raw": {}}


def test_normalize_datetime_parses_exif_format() -> None:
    normalized = MetadataExtractionService.normalize_datetime("2023:08:10 14:30:00")
    assert normalized == datetime(2023, 8, 10, 14, 30)


def test_metadata_extraction_builds_photo_with_normalized_datetime(tmp_path: Path) -> None:
    dummy_image = tmp_path / "photo.jpg"
    dummy_image.write_bytes(b"placeholder")

    service = MetadataExtractionService(
        filesystem=DummyFileSystemGateway(), exif_adapter=DummyExifAdapter("2023-08-10 14:30:00")
    )

    photo = service.extract_photo(dummy_image)

    assert isinstance(photo, Photo)
    assert photo.capture_datetime == datetime(2023, 8, 10, 14, 30)
    assert photo.checksum == "checksum"
