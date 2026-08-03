from abc import ABC, abstractmethod
from typing import Callable

from ..models.requests import (
    AudioDownloadRequest,
    AudioExtractRequest,
    AudioProbeResult,
    PlaylistDownloadRequest,
    VideoDownloadRequest,
)

ProgressHook = Callable[[dict], None]


class IVideoDownloader(ABC):
    @abstractmethod
    def download(self, request: VideoDownloadRequest, progress_hook: ProgressHook) -> None: ...


class IPlaylistDownloader(ABC):
    @abstractmethod
    def download(self, request: PlaylistDownloadRequest, progress_hook: ProgressHook) -> None: ...


class IAudioDownloader(ABC):
    @abstractmethod
    def download(self, request: AudioDownloadRequest, progress_hook: ProgressHook) -> None: ...

    @abstractmethod
    def probe(self, request: AudioDownloadRequest) -> AudioProbeResult:
        """Inspect the URL without downloading: resolve the song title and
        the exact .mp3 path that a download would produce."""
        ...


class IAudioExtractor(ABC):
    @abstractmethod
    def extract(self, request: AudioExtractRequest) -> None: ...
