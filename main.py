import sys

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication

from app.services.audio_extractor import YtDlpAudioDownloader
from app.ui.main_window import MainWindow
from app.ui.styles import STYLESHEET


def main() -> None:
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(STYLESHEET)

    window = MainWindow(audio_downloader=YtDlpAudioDownloader())
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
