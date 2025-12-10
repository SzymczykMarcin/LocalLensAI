from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple


GpsCoordinates = Tuple[float, float]


@dataclass(order=True)
class Photo:
    """Represents a photo and its core metadata."""

    sort_index: datetime = field(init=False, repr=False)
    path: Path
    checksum: Optional[str] = None
    capture_datetime: Optional[datetime] = None
    gps_coordinates: Optional[GpsCoordinates] = None
    exif_data: Dict[str, object] = field(default_factory=dict)
    original_folder: Optional[str] = None

    def __post_init__(self) -> None:
        self.sort_index = self.capture_datetime or datetime.min

    def canonical_id(self) -> str:
        """Return a canonical identifier for the photo using checksum or path."""
        if self.checksum:
            return self.checksum
        return str(self.path.resolve())

    def update_checksum(self, checksum: str) -> None:
        """Update the photo checksum."""
        self.checksum = checksum

    def update_capture_datetime(self, capture_datetime: Optional[datetime]) -> None:
        self.capture_datetime = capture_datetime
        self.sort_index = capture_datetime or datetime.min

    def update_gps(self, gps_coordinates: Optional[GpsCoordinates]) -> None:
        self.gps_coordinates = gps_coordinates

    def add_exif_data(self, exif_data: Dict[str, object]) -> None:
        self.exif_data.update(exif_data)
