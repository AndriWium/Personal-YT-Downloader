# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for YT Downloader.
# Build with:  pyinstaller YT-Downloader.spec
# Or just double-click build_exe.bat

import os
from PyInstaller.utils.hooks import collect_all

# yt-dlp loads many extractors dynamically; pull them all in.
datas, binaries, hiddenimports = collect_all("yt_dlp")

# Bundle ffmpeg.exe automatically if it sits next to this spec file.
if os.path.exists("ffmpeg.exe"):
    binaries += [("ffmpeg.exe", ".")]

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="YT-Downloader",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    runtime_tmpdir=None,
    console=False,          # windowed app, no console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
