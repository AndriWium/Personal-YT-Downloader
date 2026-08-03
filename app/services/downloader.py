import yt_dlp

from ..models.requests import PlaylistDownloadRequest, VideoDownloadRequest
from .interfaces import IPlaylistDownloader, IVideoDownloader, ProgressHook


class YtDlpVideoDownloader(IVideoDownloader):
    def download(self, request: VideoDownloadRequest, progress_hook: ProgressHook) -> None:
        opts = {
            "format": request.quality,
            "outtmpl": str(request.output_dir / "%(title)s.%(ext)s"),
            "progress_hooks": [progress_hook],
            "merge_output_format": "mp4",
            "quiet": True,
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([request.url])


class YtDlpPlaylistDownloader(IPlaylistDownloader):
    def download(self, request: PlaylistDownloadRequest, progress_hook: ProgressHook) -> None:
        opts = {
            "outtmpl": str(
                request.output_dir / "%(playlist)s" / "%(playlist_index)s - %(title)s.%(ext)s"
            ),
            "progress_hooks": [progress_hook],
            "merge_output_format": "mp4",
            "quiet": True,
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([request.url])
