from pathlib import Path

from PyQt6.QtWidgets import QComboBox, QVBoxLayout

from ...models.requests import VideoDownloadRequest
from ...services.interfaces import IVideoDownloader
from ...workers.download_worker import VideoDownloadWorker
from .base_tab import BaseTab

_QUALITY_OPTIONS: dict[str, str] = {
    "Best Available": "bestvideo+bestaudio/best",
    "1080p": "bestvideo[height<=1080]+bestaudio/best",
    "720p": "bestvideo[height<=720]+bestaudio/best",
    "480p": "bestvideo[height<=480]+bestaudio/best",
    "360p": "bestvideo[height<=360]+bestaudio/best",
}


class VideoTab(BaseTab):
    def __init__(self, downloader: IVideoDownloader) -> None:
        super().__init__()
        self._downloader = downloader
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(14)

        root.addLayout(self._header("Download Video", "Save a YouTube video in your preferred quality."))
        root.addSpacing(6)

        root.addWidget(self._field_label("Video URL"))
        self._url = self._url_field("https://www.youtube.com/watch?v=…")
        root.addWidget(self._url)

        root.addWidget(self._field_label("Quality"))
        self._quality = QComboBox()
        for label in _QUALITY_OPTIONS:
            self._quality.addItem(label)
        root.addWidget(self._quality)

        root.addWidget(self._field_label("Output Folder"))
        dir_row, self._dir, browse = self._dir_row()
        browse.clicked.connect(lambda: self._browse_dir(self._dir))
        root.addLayout(dir_row)

        root.addSpacing(6)

        from PyQt6.QtWidgets import QPushButton
        self._download_btn = QPushButton("Download Video")
        self._download_btn.setObjectName("primary_btn")
        self._download_btn.clicked.connect(self._start_download)
        root.addWidget(self._download_btn)

        progress_layout, self._bar, self._status = self._progress_section()
        root.addLayout(progress_layout)

        root.addItem(self._spacer())

    def _start_download(self) -> None:
        ok = self._validate(
            {
                self._url.text(): "Please enter a video URL.",
                self._dir.text(): "Please select an output folder.",
            },
            self._status,
        )
        if not ok:
            return

        request = VideoDownloadRequest(
            url=self._url.text().strip(),
            output_dir=Path(self._dir.text()),
            quality=_QUALITY_OPTIONS[self._quality.currentText()],
        )
        worker = VideoDownloadWorker(self._downloader, request)
        self._start_worker(worker, self._download_btn, self._bar, self._status)
