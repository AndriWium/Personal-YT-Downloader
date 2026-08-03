from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)

from ..services.interfaces import IAudioDownloader
from .downloader_view import DownloaderView


class MainWindow(QMainWindow):
    def __init__(self, audio_downloader: IAudioDownloader) -> None:
        super().__init__()
        self._setup_window()
        self._build_ui(audio_downloader)

    def _setup_window(self) -> None:
        self.setWindowTitle("YT Downloader")
        # Compact: comfortably small without text overlapping.
        self.setMinimumSize(380, 460)
        self.resize(440, 500)

    def _build_ui(self, audio_downloader: IAudioDownloader) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root = QVBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_header())
        root.addWidget(DownloaderView(audio_downloader))

    def _build_header(self) -> QWidget:
        bar = QWidget()
        bar.setFixedHeight(48)
        bar.setStyleSheet(
            "background-color: #0a0a14; border-bottom: 1px solid #1e1e38;"
        )

        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(8)

        logo = QLabel("▶")
        logo.setStyleSheet(
            "color: #7c3aed; font-size: 15px; background: transparent; border: none;"
        )

        title = QLabel("YT Downloader")
        title.setStyleSheet(
            "color: #e2e8f0; font-size: 14px; font-weight: 700; "
            "background: transparent; border: none;"
        )

        layout.addWidget(logo)
        layout.addWidget(title)
        layout.addStretch()

        return bar
