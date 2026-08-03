# YT Downloader

A small Windows desktop app for pulling a single YouTube video's audio down as an MP3. Paste a link, pick a bitrate, get a song — no ads, no bundled toolbars, no playlist scraping.

## Features

- Paste a single video link — playlist links are rejected on purpose, this is a one-song-at-a-time tool
- Choose a bitrate: 320 / 192 / 128 kbps
- Warns before overwriting a file you've already downloaded
- Packaged as a standalone `.exe` with PyInstaller — no Python install needed to run it

## Stack

- **Python** + **PyQt6** for the UI
- **yt-dlp** to resolve and download audio streams
- **ffmpeg** for the audio conversion (not bundled — see below)
- **PyInstaller** to package everything into a single `.exe`

## Running from source

```bash
pip install -r requirements.txt
python main.py
```

Requires [ffmpeg](https://ffmpeg.org/download.html) on your `PATH`, or an `ffmpeg.exe` sitting next to the script.

## Building the .exe

Double-click `build_exe.bat`, or run:

```bash
pip install -r requirements.txt pyinstaller
python -m PyInstaller --noconfirm YT-Downloader.spec
```

The built app lands at `dist\YT-Downloader.exe`. MP3 conversion still needs ffmpeg — either have it on `PATH`, or drop `ffmpeg.exe` next to the `.exe` (or next to this repo before building, and the spec will bundle it in automatically).

## A note on use

This is a personal tool for things like saving your own uploads, Creative Commons / public-domain audio, or clips you otherwise have the rights to — not a way around YouTube's Terms of Service. You're responsible for how you use it and for whatever content you point it at.

## License

MIT — see [LICENSE](LICENSE).
