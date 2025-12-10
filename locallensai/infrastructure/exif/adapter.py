from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

from PIL import Image, ExifTags

GpsTuple = Tuple[float, float]


class ExifMetadataAdapter:
    """Adapter responsible for interacting with Pillow to read EXIF data."""

    def is_image_valid(self, file_path: Path) -> bool:
        try:
            with Image.open(file_path) as image:
                image.verify()
            return True
        except Exception:
            return False

    def extract_metadata(self, file_path: Path) -> Dict[str, object]:
        with Image.open(file_path) as image:
            exif_data = image.getexif()

        exif_dict: Dict[str, object] = {}
        if exif_data:
            for tag_id, value in exif_data.items():
                tag_name = ExifTags.TAGS.get(tag_id, str(tag_id))
                exif_dict[tag_name] = value

        datetime_value = self._extract_datetime(exif_dict)
        gps_coordinates = self._extract_gps(exif_data) if exif_data else None

        return {"datetime": datetime_value, "gps": gps_coordinates, "raw": exif_dict}

    def _extract_datetime(self, exif_dict: Dict[str, object]) -> Optional[object]:
        for key in ("DateTimeOriginal", "DateTimeDigitized", "DateTime"):
            if key in exif_dict:
                value = exif_dict[key]
                if isinstance(value, bytes):
                    return value.decode(errors="ignore")
                return value
        return None

    def _extract_gps(self, exif_data) -> Optional[GpsTuple]:
        gps_info = exif_data.get_ifd(ExifTags.IFD.GPSInfo)
        if not gps_info:
            return None

        gps_map = {ExifTags.GPSTAGS.get(key, key): value for key, value in gps_info.items()}
        lat = gps_map.get("GPSLatitude")
        lat_ref = gps_map.get("GPSLatitudeRef")
        lon = gps_map.get("GPSLongitude")
        lon_ref = gps_map.get("GPSLongitudeRef")

        if not (lat and lat_ref and lon and lon_ref):
            return None

        latitude = self._convert_to_degrees(lat)
        longitude = self._convert_to_degrees(lon)

        if lat_ref != "N":
            latitude = -latitude
        if lon_ref != "E":
            longitude = -longitude
        return latitude, longitude

    def _convert_to_degrees(self, value) -> float:
        try:
            d, m, s = value
            return float(d) + float(m) / 60 + float(s) / 3600
        except Exception:
            return 0.0
