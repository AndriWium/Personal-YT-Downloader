from PyQt6.QtCore import QThread, pyqtSignal


class BaseWorker(QThread):
    progress = pyqtSignal(int, str)  # (percent 0-100, status text)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def _build_yt_hook(self):
        def hook(d: dict) -> None:
            if d["status"] == "downloading":
                downloaded = d.get("downloaded_bytes", 0)
                total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
                speed = d.get("_speed_str", "").strip()
                eta = d.get("_eta_str", "").strip()
                if total:
                    pct = min(99, int(downloaded / total * 100))
                    self.progress.emit(pct, f"{speed}  •  ETA {eta}")
                else:
                    self.progress.emit(0, f"Downloading…  {speed}")
            elif d["status"] == "finished":
                self.progress.emit(99, "Processing…")

        return hook
