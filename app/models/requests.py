from dataclasses import dataclass
from pathlib import Path


@dataclass
class VideoDownloadRequest:
    url: str
    output_dir: Path
    quality: str = "bestvideo+bestaudio/best"


@dataclass
class PlaylistDownloadRequest:
    url: str
    output_dir: Path


@dataclass
class AudioDownloadRequest:
    url: str
    output_dir: Path
    bitrate: str = "192"


@dataclass
class AudioExtractRequest:
    input_file: Path
    output_file: Path


@dataclass
class AudioProbeResult:
    """Result of inspecting a URL before download."""

    title: str
    output_file: Path
