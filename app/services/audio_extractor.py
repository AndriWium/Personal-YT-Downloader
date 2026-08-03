import subprocess
import sys
from pathlib import Path

import yt_dlp

from ..models.requests import (
    AudioDownloadRequest,
    AudioExtractRequest,
    AudioProbeResult,
)
from .interfaces import IAudioDownloader, IAudioExtractor, ProgressHook


def _find_ffmpeg() -> str | None:
    """Locate a bundled/sibling ffmpeg(.exe) so the packaged .exe works
    without ffmpeg on PATH. Returns a directory, or None to fall back to PATH."""
    candidates: list[Path] = []
    bundle = getattr(sys, "_MEIPASS", None)
    if bundle:
        candidates.append(Path(bundle))
    if getattr(sys, "frozen", False):
        candidates.append(Path(sys.executable).parent)
    name = "ffmpeg.exe" if sys.platform == "win32" else "ffmpeg"
    for directory in candidates:
        if (directory / name).exists():
            return str(directory)
    return None


_FFMPEG_DIR = _find_ffmpeg()


class YtDlpAudioDownloader(IAudioDownloader):
    def probe(self, request: AudioDownloadRequest) -> AudioProbeResult:
        opts = {
            "outtmpl": str(request.output_dir / "%(title)s.%(ext)s"),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(request.url, download=False)
            # If a playlist slipped through, only consider the first entry.
            if info.get("entries"):
                info = info["entries"][0]
            title = info.get("title", "audio")
            base = Path(ydl.prepare_filename(info))
        output_file = base.with_suffix(".mp3")
        return AudioProbeResult(title=title, output_file=output_file)

    def download(self, request: AudioDownloadRequest, progress_hook: ProgressHook) -> None:
        opts = {
            "format": "bestaudio/best",
            "outtmpl": str(request.output_dir / "%(title)s.%(ext)s"),
            "progress_hooks": [progress_hook],
            "noplaylist": True,
            "overwrites": True,
            "quiet": True,
            "no_warnings": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": request.bitrate,
                }
            ],
        }
        if _FFMPEG_DIR:
            opts["ffmpeg_location"] = _FFMPEG_DIR
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([request.url])


class FfmpegAudioExtractor(IAudioExtractor):
    def extract(self, request: AudioExtractRequest) -> None:
        cmd = [
            "ffmpeg",
            "-i", str(request.input_file),
            "-q:a", "0",
            "-map", "a",
            str(request.output_file),
            "-y",
        ]
        if sys.platform == "win32":
            cmd = ["cmd.exe", "/c"] + cmd
        subprocess.check_call(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
