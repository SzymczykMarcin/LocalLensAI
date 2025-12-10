from pathlib import Path

from PIL import Image

from locallensai.infrastructure.exif.adapter import ExifMetadataAdapter


def test_is_image_valid_handles_valid_and_corrupted_images(tmp_path: Path) -> None:
    adapter = ExifMetadataAdapter()

    valid_path = tmp_path / "valid.jpg"
    image = Image.new("RGB", (10, 10), color="red")
    image.save(valid_path)

    corrupted_path = tmp_path / "corrupted.jpg"
    corrupted_path.write_bytes(b"not an image")

    assert adapter.is_image_valid(valid_path) is True
    assert adapter.is_image_valid(corrupted_path) is False
