from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from .photo import Photo


@dataclass
class Event:
    """Placeholder representation for a collection of related photos."""

    event_id: str
    event_type: Optional[str] = None
    start_datetime: Optional[datetime] = None
    end_datetime: Optional[datetime] = None
    location: Optional[str] = None
    photos: List[Photo] = field(default_factory=list)

    def add_photo(self, photo: Photo) -> None:
        self.photos.append(photo)

    def sort_photos(self) -> None:
        self.photos.sort()
