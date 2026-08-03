import re
from pathlib import Path

from PyQt6.QtWidgets import (
    QComboBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ..models.requests import AudioDownloadRequest, AudioProbeResult
from ..services.interfaces import IAudioDownloader
from ..workers.extract_worker import AudioDownloadWorker, AudioProbeWorker

_BITRATE_OPTIONS = {"320 kbps": "320", "192 kbps": "192", "128 kbps": "128"}

# A single-video YouTube link. Playlist-only links are rejected separately.
_YT_PATTERN = re.compile(
    r"^(https?://)?(www\.)?(youtube\.com/(watch\?|shorts/|live/)|youtu\.be/)",
    re.IGNORECASE,
)


class DownloaderView(QWidget):
    """Single-purpose YouTube → MP3 downloader."""

    def __init__(self, downloader: IAudioDownloader) -> None:
        super().__init__()
        self._downloader = downloader
        self._probe_worker: AudioProbeWorker | None = None
        self._dl_worker: AudioDownloadWorker | None = None
        self._pending_title = ""
        self._build_ui()

    # ── UI ─────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(22, 20, 22, 20)
        root.setSpacing(12)

        title = QLabel("YouTube → MP3")
        title.setObjectName("tab_header")
        title.setWordWrap(True)
        root.addWidget(title)

        subtitle = QLabel("Paste a single video link and download it as an MP3.")
        subtitle.setObjectName("tab_subtitle")
        subtitle.setWordWrap(True)
        root.addWidget(subtitle)

        root.addSpacing(4)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(18, 16, 18, 16)
        card_layout.setSpacing(10)

        card_layout.addWidget(self._field_label("Video URL"))
        self._url = QLineEdit()
        self._url.setPlaceholderText("https://www.youtube.com/watch?v=…")
        self._url.textChanged.connect(self._on_url_changed)
        self._url.returnPressed.connect(self._start_download)
        card_layout.addWidget(self._url)

        card_layout.addWidget(self._field_label("Quality"))
        self._bitrate = QComboBox()
        for label in _BITRATE_OPTIONS:
            self._bitrate.addItem(label)
        card_layout.addWidget(self._bitrate)

        card_layout.addWidget(self._field_label("Output Folder"))
        dir_row = QHBoxLayout()
        dir_row.setSpacing(8)
        self._dir = QLineEdit()
        self._dir.setPlaceholderText("Choose output folder…")
        self._dir.setReadOnly(True)
        browse = QPushButton("Browse")
        browse.setObjectName("browse_btn")
        browse.setFixedWidth(80)
        browse.clicked.connect(self._browse_dir)
        dir_row.addWidget(self._dir)
        dir_row.addWidget(browse)
        card_layout.addLayout(dir_row)

        self._dl_btn = QPushButton("Download as MP3")
        self._dl_btn.setObjectName("primary_btn")
        self._dl_btn.clicked.connect(self._start_download)
        card_layout.addWidget(self._dl_btn)

        self._bar = QProgressBar()
        self._bar.setValue(0)
        self._bar.setTextVisible(False)
        card_layout.addWidget(self._bar)

        self._status = QLabel("")
        self._status.setObjectName("status_label")
        self._status.setWordWrap(True)
        card_layout.addWidget(self._status)

        root.addWidget(card)
        root.addStretch()

    def _field_label(self, text: str) -> QLabel:
        lbl = QLabel(text.upper())
        lbl.setObjectName("field_label")
        return lbl

    # ── Field interactions ─────────────────────────────────────────────

    def _browse_dir(self) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if path:
            self._dir.setText(path)

    def _on_url_changed(self, _text: str) -> None:
        # Clear any leftover error/success state when a new URL is entered.
        self._status.clear()
        self._status.setObjectName("status_label")
        self._bar.setValue(0)

    # ── Validation ─────────────────────────────────────────────────────

    @staticmethod
    def _is_playlist_link(url: str) -> bool:
        return "playlist?list=" in url or "/playlist" in url

    def _validate(self) -> bool:
        url = self._url.text().strip()
        if not url:
            self._popup_error("Please enter a video URL.")
            return False
        if self._is_playlist_link(url):
            self._popup_error(
                "That looks like a playlist link. Please paste a single video URL."
            )
            return False
        if not _YT_PATTERN.match(url):
            self._popup_error("Please enter a valid YouTube video link.")
            return False
        if not self._dir.text().strip():
            self._popup_error("Please select an output folder.")
            return False
        return True

    # ── Download flow ──────────────────────────────────────────────────

    def _start_download(self) -> None:
        if self._is_busy():
            return
        if not self._validate():
            return

        request = self._build_request()
        self._dl_btn.setEnabled(False)
        self._bar.setValue(0)
        self._set_status("Checking link…", "neutral")

        self._probe_worker = AudioProbeWorker(self._downloader, request)
        self._probe_worker.result.connect(lambda res: self._on_probed(res, request))
        self._probe_worker.error.connect(self._on_probe_error)
        self._probe_worker.start()

    def _on_probed(self, result: AudioProbeResult, request: AudioDownloadRequest) -> None:
        # Duplicate check: ask before overwriting an existing file.
        if result.output_file.exists():
            answer = QMessageBox.question(
                self,
                "Song already downloaded",
                f"“{result.title}” already exists in this folder.\n\n"
                "Download again and overwrite it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if answer != QMessageBox.StandardButton.Yes:
                self._dl_btn.setEnabled(True)
                self._set_status("Cancelled — file kept.", "neutral")
                return

        self._pending_title = result.title
        self._set_status(f"Downloading: {result.title}", "neutral")

        self._dl_worker = AudioDownloadWorker(self._downloader, request)
        self._dl_worker.progress.connect(self._on_progress)
        self._dl_worker.finished.connect(self._on_finished)
        self._dl_worker.error.connect(self._on_download_error)
        self._dl_worker.start()

    def _build_request(self) -> AudioDownloadRequest:
        return AudioDownloadRequest(
            url=self._url.text().strip(),
            output_dir=Path(self._dir.text()),
            bitrate=_BITRATE_OPTIONS[self._bitrate.currentText()],
        )

    # ── Worker callbacks ───────────────────────────────────────────────

    def _on_progress(self, pct: int, text: str) -> None:
        self._bar.setValue(pct)
        if text:
            self._set_status(text, "neutral")

    def _on_finished(self) -> None:
        self._bar.setValue(100)
        self._dl_btn.setEnabled(True)
        title = self._pending_title or "your song"
        self._set_status(f"Downloaded: {title}", "success")
        QMessageBox.information(
            self,
            "Download complete",
            f"“{title}” was downloaded successfully.",
        )
        # Clear the link and re-focus the input for the next song.
        self._url.clear()
        self._url.setFocus()

    def _on_probe_error(self, msg: str) -> None:
        self._dl_btn.setEnabled(True)
        self._bar.setValue(0)
        self._popup_error(f"Couldn't read that link.\n\n{msg}")

    def _on_download_error(self, msg: str) -> None:
        self._dl_btn.setEnabled(True)
        self._bar.setValue(0)
        self._popup_error(f"Download failed.\n\n{msg}")

    # ── Helpers ────────────────────────────────────────────────────────

    def _is_busy(self) -> bool:
        for w in (self._probe_worker, self._dl_worker):
            if w is not None and w.isRunning():
                return True
        return False

    def _popup_error(self, message: str) -> None:
        self._set_status("", "neutral")
        QMessageBox.warning(self, "Heads up", message)

    def _set_status(self, text: str, kind: str) -> None:
        self._status.setText(text)
        name = {"success": "status_success", "error": "status_error"}.get(
            kind, "status_label"
        )
        self._status.setObjectName(name)
        self._status.style().unpolish(self._status)
        self._status.style().polish(self._status)
