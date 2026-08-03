from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
    QWidget,
)

from ...workers.base_worker import BaseWorker


class BaseTab(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._worker: BaseWorker | None = None

    # ── Layout helpers ─────────────────────────────────────────────────

    def _header(self, title: str, subtitle: str) -> QVBoxLayout:
        layout = QVBoxLayout()
        layout.setSpacing(4)
        h = QLabel(title)
        h.setObjectName("tab_header")
        s = QLabel(subtitle)
        s.setObjectName("tab_subtitle")
        layout.addWidget(h)
        layout.addWidget(s)
        return layout

    def _field_label(self, text: str) -> QLabel:
        lbl = QLabel(text.upper())
        lbl.setObjectName("field_label")
        return lbl

    def _url_field(self, placeholder: str) -> QLineEdit:
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        return field

    def _dir_row(self) -> tuple[QHBoxLayout, QLineEdit, QPushButton]:
        layout = QHBoxLayout()
        layout.setSpacing(8)
        field = QLineEdit()
        field.setPlaceholderText("Choose output folder…")
        field.setReadOnly(True)
        btn = QPushButton("Browse")
        btn.setObjectName("browse_btn")
        btn.setFixedWidth(80)
        layout.addWidget(field)
        layout.addWidget(btn)
        return layout, field, btn

    def _file_row(self, placeholder: str) -> tuple[QHBoxLayout, QLineEdit, QPushButton]:
        layout = QHBoxLayout()
        layout.setSpacing(8)
        field = QLineEdit()
        field.setPlaceholderText(placeholder)
        field.setReadOnly(True)
        btn = QPushButton("Browse")
        btn.setObjectName("file_btn")
        btn.setFixedWidth(80)
        layout.addWidget(field)
        layout.addWidget(btn)
        return layout, field, btn

    def _progress_section(self) -> tuple[QVBoxLayout, QProgressBar, QLabel]:
        layout = QVBoxLayout()
        layout.setSpacing(6)
        bar = QProgressBar()
        bar.setValue(0)
        bar.setTextVisible(False)
        status = QLabel("")
        status.setObjectName("status_label")
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(bar)
        layout.addWidget(status)
        return layout, bar, status

    def _spacer(self) -> QSpacerItem:
        return QSpacerItem(0, 0, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

    # ── File dialogs ───────────────────────────────────────────────────

    def _browse_dir(self, field: QLineEdit) -> None:
        path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if path:
            field.setText(path)

    def _browse_file(self, field: QLineEdit, filter_str: str = "Video files (*.mp4 *.mkv *.webm *.avi)") -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select File", "", filter_str)
        if path:
            field.setText(path)

    # ── Worker lifecycle ───────────────────────────────────────────────

    def _start_worker(
        self,
        worker: BaseWorker,
        btn: QPushButton,
        bar: QProgressBar,
        status: QLabel,
    ) -> None:
        if self._worker and self._worker.isRunning():
            return
        self._worker = worker
        btn.setEnabled(False)
        bar.setValue(0)
        self._set_status(status, "Starting…", "neutral")
        worker.progress.connect(lambda p, s: self._on_progress(p, s, bar, status))
        worker.finished.connect(lambda: self._on_finished(btn, status))
        worker.error.connect(lambda e: self._on_error(e, btn, bar, status))
        worker.start()

    def _on_progress(self, pct: int, text: str, bar: QProgressBar, status: QLabel) -> None:
        bar.setValue(pct)
        self._set_status(status, text, "neutral")

    def _on_finished(self, btn: QPushButton, status: QLabel) -> None:
        btn.setEnabled(True)
        self._set_status(status, status.text(), "success")

    def _on_error(self, msg: str, btn: QPushButton, bar: QProgressBar, status: QLabel) -> None:
        bar.setValue(0)
        btn.setEnabled(True)
        self._set_status(status, f"Error: {msg}", "error")

    # ── Validation ─────────────────────────────────────────────────────

    def _validate(self, fields: dict[str, str], status: QLabel) -> bool:
        for value, message in fields.items():
            if not value.strip():
                self._set_status(status, message, "error")
                return False
        return True

    # ── Styling ────────────────────────────────────────────────────────

    def _set_status(self, label: QLabel, text: str, kind: str) -> None:
        label.setText(text)
        name = {"success": "status_success", "error": "status_error"}.get(kind, "status_label")
        label.setObjectName(name)
        label.setStyleSheet(label.styleSheet())  # force repaint
        label.style().unpolish(label)
        label.style().polish(label)
