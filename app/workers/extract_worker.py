from PyQt6.QtCore import pyqtSignal

from ..models.requests import AudioDownloadRequest, AudioExtractRequest
from ..services.interfaces import IAudioDownloader, IAudioExtractor
from .base_worker import BaseWorker


class AudioProbeWorker(BaseWorker):
    """Resolve a URL's song title + target path without downloading."""

    result = pyqtSignal(object)  # emits AudioProbeResult

    def __init__(self, downloader: IAudioDownloader, request: AudioDownloadRequest) -> None:
        super().__init__()
        self._downloader = downloader
        self._request = request

    def run(self) -> None:
        try:
            self.result.emit(self._downloader.probe(self._request))
        except Exception as exc:
            self.error.emit(str(exc))


class AudioDownloadWorker(BaseWorker):
    def __init__(self, downloader: IAudioDownloader, request: AudioDownloadRequest) -> None:
        super().__init__()
        self._downloader = downloader
        self._request = request

    def run(self) -> None:
        try:
            self._downloader.download(self._request, self._build_yt_hook())
            self.progress.emit(100, "Download complete!")
            self.finished.emit()
        except Exception as exc:
            self.error.emit(str(exc))


class AudioExtractWorker(BaseWorker):
    def __init__(self, extractor: IAudioExtractor, request: AudioExtractRequest) -> None:
        super().__init__()
        self._extractor = extractor
        self._request = request

    def run(self) -> None:
        try:
            self.progress.emit(0, "Extracting audio…")
            self._extractor.extract(self._request)
            self.progress.emit(100, "Extraction complete!")
            self.finished.emit()
        except Exception as exc:
            self.error.emit(str(exc))
