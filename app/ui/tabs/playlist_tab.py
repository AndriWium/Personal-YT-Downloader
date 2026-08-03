from pathlib import Path

from PyQt6.QtWidgets import QPushButton, QVBoxLayout

from ...models.requests import PlaylistDownloadRequest
from ...services.interfaces import IPlaylistDownloader
from ...workers.download_worker import PlaylistDownloadWorker
from .base_tab import BaseTab


class PlaylistTab(BaseTab):
    def __init__(self, downloader: IPlaylistDownloader) -> None:
        super().__init__()
        self._downloader = downloader
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(14)

        root.addLayout(
            self._header(
                "Download Playlist",
                "Download every video in a YouTube playlist into a named subfolder.",
            )
        )
        root.addSpacing(6)

        root.addWidget(self._field_label("Playlist URL"))
        self._url = self._url_field("https://www.youtube.com/playlist?list=…")
        root.addWidget(self._url)

        root.addWidget(self._field_label("Output Folder"))
        dir_row, self._dir, browse = self._dir_row()
        browse.clicked.connect(lambda: self._browse_dir(self._dir))
        root.addLayout(dir_row)

        root.addSpacing(6)

        self._download_btn = QPushButton("Download Playlist")
        self._download_btn.setObjectName("primary_btn")
        self._download_btn.clicked.connect(self._start_download)
        root.addWidget(self._download_btn)

        progress_layout, self._bar, self._status = self._progress_section()
        root.addLayout(progress_layout)

        root.addItem(self._spacer())

    def _start_download(self) -> None:
        ok = self._validate(
            {
                self._url.text(): "Please enter a playlist URL.",
                self._dir.text(): "Please select an output folder.",
            },
            self._status,
        )
        if not ok:
            return

        request = PlaylistDownloadRequest(
            url=self._url.text().strip(),
            output_dir=Path(self._dir.text()),
        )
        worker = PlaylistDownloadWorker(self._downloader, request)
        self._start_worker(worker, self._download_btn, self._bar, self._status)
