STYLESHEET = """
/* ── Base ─────────────────────────────────────────────────── */
QMainWindow, QWidget {
    background-color: #0f0f1a;
    color: #e2e8f0;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 13px;
}

/* ── Tab widget ───────────────────────────────────────────── */
QTabWidget::pane {
    border: none;
    background-color: #13131f;
}

QTabBar {
    background-color: #0a0a14;
}

QTabBar::tab {
    background-color: transparent;
    color: #64748b;
    padding: 14px 32px;
    font-size: 13px;
    font-weight: 500;
    border: none;
    border-bottom: 2px solid transparent;
}

QTabBar::tab:selected {
    color: #a78bfa;
    border-bottom: 2px solid #7c3aed;
}

QTabBar::tab:hover:!selected {
    color: #cbd5e1;
    background-color: #ffffff08;
}

/* ── Section frames (cards) ───────────────────────────────── */
QFrame#card {
    background-color: #1a1a2e;
    border: 1px solid #2d2d4e;
    border-radius: 12px;
}

/* ── Typography ───────────────────────────────────────────── */
QLabel#tab_header {
    font-size: 22px;
    font-weight: 700;
    color: #f1f5f9;
    background: transparent;
}

QLabel#tab_subtitle {
    color: #475569;
    font-size: 13px;
    background: transparent;
}

QLabel#field_label {
    color: #64748b;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.8px;
    background: transparent;
}

QLabel#section_header {
    color: #94a3b8;
    font-size: 13px;
    font-weight: 600;
    background: transparent;
}

QLabel#status_label {
    color: #64748b;
    font-size: 12px;
    background: transparent;
}

QLabel#status_success {
    color: #4ade80;
    font-size: 12px;
    background: transparent;
}

QLabel#status_error {
    color: #f87171;
    font-size: 12px;
    background: transparent;
}

/* ── Inputs ───────────────────────────────────────────────── */
QLineEdit {
    background-color: #1a1a2e;
    border: 1px solid #2d2d4e;
    border-radius: 8px;
    padding: 10px 14px;
    color: #e2e8f0;
    font-size: 13px;
    selection-background-color: #7c3aed;
    min-height: 18px;
}

QLineEdit:focus {
    border-color: #7c3aed;
    background-color: #1f1f38;
}

QLineEdit:read-only {
    color: #64748b;
}

/* ── ComboBox ─────────────────────────────────────────────── */
QComboBox {
    background-color: #1a1a2e;
    border: 1px solid #2d2d4e;
    border-radius: 8px;
    padding: 10px 14px;
    color: #e2e8f0;
    font-size: 13px;
    min-height: 18px;
}

QComboBox:focus {
    border-color: #7c3aed;
}

QComboBox::drop-down {
    border: none;
    width: 28px;
}

QComboBox::down-arrow {
    image: none;
    border-left: 5px solid transparent;
    border-right: 5px solid transparent;
    border-top: 6px solid #64748b;
    margin-right: 10px;
}

QComboBox QAbstractItemView {
    background-color: #1a1a2e;
    border: 1px solid #2d2d4e;
    border-radius: 8px;
    selection-background-color: #7c3aed;
    color: #e2e8f0;
    padding: 4px;
    outline: none;
}

QComboBox QAbstractItemView::item {
    padding: 8px 14px;
    border-radius: 4px;
}

/* ── Buttons ──────────────────────────────────────────────── */
QPushButton#primary_btn {
    background-color: #7c3aed;
    color: #ffffff;
    border: none;
    border-radius: 8px;
    padding: 12px 24px;
    font-size: 13px;
    font-weight: 600;
    min-height: 20px;
}

QPushButton#primary_btn:hover {
    background-color: #6d28d9;
}

QPushButton#primary_btn:pressed {
    background-color: #5b21b6;
}

QPushButton#primary_btn:disabled {
    background-color: #2d2d4e;
    color: #475569;
}

QPushButton#browse_btn {
    background-color: #1a1a2e;
    color: #94a3b8;
    border: 1px solid #2d2d4e;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 12px;
    font-weight: 500;
    min-height: 18px;
}

QPushButton#browse_btn:hover {
    background-color: #2d2d4e;
    color: #e2e8f0;
    border-color: #4a4a6a;
}

QPushButton#file_btn {
    background-color: #1a1a2e;
    color: #94a3b8;
    border: 1px solid #2d2d4e;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 12px;
    font-weight: 500;
    min-height: 18px;
}

QPushButton#file_btn:hover {
    background-color: #2d2d4e;
    color: #e2e8f0;
    border-color: #4a4a6a;
}

/* ── Progress bar ─────────────────────────────────────────── */
QProgressBar {
    background-color: #1a1a2e;
    border: none;
    border-radius: 5px;
    min-height: 6px;
    max-height: 6px;
    text-align: center;
}

QProgressBar::chunk {
    background: qlineargradient(
        x1:0, y1:0, x2:1, y2:0,
        stop:0 #7c3aed,
        stop:1 #a78bfa
    );
    border-radius: 5px;
}

/* ── Scrollbar ────────────────────────────────────────────── */
QScrollBar:vertical {
    background: transparent;
    width: 6px;
    border-radius: 3px;
}

QScrollBar::handle:vertical {
    background: #2d2d4e;
    border-radius: 3px;
    min-height: 24px;
}

QScrollBar::handle:vertical:hover {
    background: #7c3aed;
}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    height: 0;
}
"""
