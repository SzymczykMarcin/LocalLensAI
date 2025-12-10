from __future__ import annotations

import hashlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generator, Iterable, Set


class FileSystemGateway(ABC):
    """Abstraction for filesystem access."""

    @abstractmethod
    def iterate_files(self, root_path: Path, extensions: Iterable[str]) -> Generator[Path, None, None]:
        """Yield files within root_path matching the given extensions."""

    @abstractmethod
    def compute_checksum(self, file_path: Path) -> str:
        """Compute a checksum for the file contents."""


class LocalFileSystemGateway(FileSystemGateway):
    """Local filesystem implementation using pathlib."""

    def iterate_files(self, root_path: Path, extensions: Iterable[str]) -> Generator[Path, None, None]:
        normalized_exts: Set[str] = {ext.lower() for ext in extensions}
        for path in root_path.rglob("*"):
            if path.is_file() and path.suffix.lower() in normalized_exts:
                yield path

    def compute_checksum(self, file_path: Path) -> str:
        sha256 = hashlib.sha256()
        with file_path.open("rb") as file_handle:
            for chunk in iter(lambda: file_handle.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
