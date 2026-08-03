from ..models.requests import PlaylistDownloadRequest, VideoDownloadRequest
from ..services.interfaces import IPlaylistDownloader, IVideoDownloader
from .base_worker import BaseWorker


class VideoDownloadWorker(BaseWorker):
    def __init__(self, downloader: IVideoDownloader, request: VideoDownloadRequest) -> None:
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


class PlaylistDownloadWorker(BaseWorker):
    def __init__(self, downloader: IPlaylistDownloader, request: PlaylistDownloadRequest) -> None:
        super().__init__()
        self._downloader = downloader
        self._request = request
        self._current = 0
        self._total = 0

    def run(self) -> None:
        try:
            self._downloader.download(self._request, self._build_playlist_hook())
            self.progress.emit(100, "Playlist download complete!")
            self.finished.emit()
        except Exception as exc:
            self.error.emit(str(exc))

    def _build_playlist_hook(self):
        def hook(d: dict) -> None:
            info = d.get("info_dict", {})
            idx = info.get("playlist_index") or info.get("playlist_autonumber", 0)
            total = info.get("n_entries", 0)
            if idx:
                self._current = idx
            if total:
                self._total = total

            speed = d.get("_speed_str", "").strip()

            if d["status"] == "downloading":
                downloaded = d.get("downloaded_bytes", 0)
                file_total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
                if self._total:
                    base_pct = (self._current - 1) / self._total
                    file_frac = (downloaded / file_total) if file_total else 0
                    pct = min(99, int((base_pct + file_frac / self._total) * 100))
                    label = f"Video {self._current}/{self._total}  •  {speed}"
                    self.progress.emit(pct, label)
                else:
                    self.progress.emit(0, f"Downloading…  {speed}")
            elif d["status"] == "finished":
                if self._total:
                    pct = min(99, int(self._current / self._total * 100))
                    self.progress.emit(pct, f"Processing {self._current}/{self._total}…")
                else:
                    self.progress.emit(99, "Processing…")

        return hook
