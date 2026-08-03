from pathlib import Path

from PyQt6.QtWidgets import (
    QComboBox,
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from ...models.requests import AudioDownloadRequest, AudioExtractRequest
from ...services.interfaces import IAudioDownloader, IAudioExtractor
from ...workers.extract_worker import AudioDownloadWorker, AudioExtractWorker
from .base_tab import BaseTab

_BITRATE_OPTIONS = {"320 kbps": "320", "192 kbps": "192", "128 kbps": "128"}


class AudioTab(BaseTab):
    def __init__(self, downloader: IAudioDownloader, extractor: IAudioExtractor) -> None:
        super().__init__()
        self._downloader = downloader
        self._extractor = extractor
        self._dl_worker = None
        self._ex_worker = None
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(32, 28, 32, 28)
        root.setSpacing(14)

        root.addLayout(
            self._header(
                "Audio",
                "Download YouTube audio as MP3, or extract audio from a local video file.",
            )
        )
        root.addSpacing(6)

        # ── Card 1: YouTube to MP3 ─────────────────────────────────────
        dl_card = self._card()
        dl_layout = QVBoxLayout(dl_card)
        dl_layout.setContentsMargins(20, 18, 20, 18)
        dl_layout.setSpacing(12)

        section_lbl = QLabel("YouTube → MP3")
        section_lbl.setObjectName("section_header")
        dl_layout.addWidget(section_lbl)

        dl_layout.addWidget(self._field_label("Video or Playlist URL"))
        self._dl_url = self._url_field("https://www.youtube.com/watch?v=…")
        dl_layout.addWidget(self._dl_url)

        dl_layout.addWidget(self._field_label("Quality"))
        self._bitrate = QComboBox()
        for label in _BITRATE_OPTIONS:
            self._bitrate.addItem(label)
        dl_layout.addWidget(self._bitrate)

        dl_layout.addWidget(self._field_label("Output Folder"))
        dir_row, self._dl_dir, dl_browse = self._dir_row()
        dl_browse.clicked.connect(lambda: self._browse_dir(self._dl_dir))
        dl_layout.addLayout(dir_row)

        self._dl_btn = QPushButton("Download as MP3")
        self._dl_btn.setObjectName("primary_btn")
        self._dl_btn.clicked.connect(self._start_audio_download)
        dl_layout.addWidget(self._dl_btn)

        dl_progress, self._dl_bar, self._dl_status = self._progress_section()
        dl_layout.addLayout(dl_progress)

        root.addWidget(dl_card)

        # ── Card 2: Extract from local file ───────────────────────────
        ex_card = self._card()
        ex_layout = QVBoxLayout(ex_card)
        ex_layout.setContentsMargins(20, 18, 20, 18)
        ex_layout.setSpacing(12)

        section_lbl2 = QLabel("Extract from Local File")
        section_lbl2.setObjectName("section_header")
        ex_layout.addWidget(section_lbl2)

        ex_layout.addWidget(self._field_label("Input Video File"))
        file_row, self._ex_input, ex_file_btn = self._file_row("Select a video file…")
        ex_file_btn.clicked.connect(lambda: self._browse_file(self._ex_input))
        ex_layout.addLayout(file_row)

        ex_layout.addWidget(self._field_label("Output File Name"))
        self._ex_output = self._url_field("output.mp3")
        ex_layout.addWidget(self._ex_output)

        self._ex_btn = QPushButton("Extract Audio")
        self._ex_btn.setObjectName("primary_btn")
        self._ex_btn.clicked.connect(self._start_extraction)
        ex_layout.addWidget(self._ex_btn)

        ex_progress, self._ex_bar, self._ex_status = self._progress_section()
        ex_layout.addLayout(ex_progress)

        root.addWidget(ex_card)
        root.addItem(self._spacer())

    def _card(self) -> QFrame:
        frame = QFrame()
        frame.setObjectName("card")
        return frame

    # ── Download handlers ──────────────────────────────────────────────

    def _start_audio_download(self) -> None:
        ok = self._validate(
            {
                self._dl_url.text(): "Please enter a URL.",
                self._dl_dir.text(): "Please select an output folder.",
            },
            self._dl_status,
        )
        if not ok:
            return

        request = AudioDownloadRequest(
            url=self._dl_url.text().strip(),
            output_dir=Path(self._dl_dir.text()),
            bitrate=_BITRATE_OPTIONS[self._bitrate.currentText()],
        )
        self._dl_worker = AudioDownloadWorker(self._downloader, request)
        self._start_worker(self._dl_worker, self._dl_btn, self._dl_bar, self._dl_status)

    def _start_extraction(self) -> None:
        ok = self._validate(
            {
                self._ex_input.text(): "Please select an input video file.",
                self._ex_output.text(): "Please enter an output file name.",
            },
            self._ex_status,
        )
        if not ok:
            return

        input_path = Path(self._ex_input.text())
        output_name = self._ex_output.text().strip()
        if not output_name.endswith(".mp3"):
            output_name += ".mp3"
        output_path = input_path.parent / output_name

        request = AudioExtractRequest(input_file=input_path, output_file=output_path)
        self._ex_worker = AudioExtractWorker(self._extractor, request)
        self._start_worker(self._ex_worker, self._ex_btn, self._ex_bar, self._ex_status)

    # AudioTab manages two independent workers — override to use the right one
    def _start_worker(self, worker, btn, bar, status):  # type: ignore[override]
        if worker and worker.isRunning():
            return
        btn.setEnabled(False)
        bar.setValue(0)
        self._set_status(status, "Starting…", "neutral")
        worker.progress.connect(lambda p, s: self._on_progress(p, s, bar, status))
        worker.finished.connect(lambda: self._on_finished(btn, status))
        worker.error.connect(lambda e: self._on_error(e, btn, bar, status))
        worker.start()
