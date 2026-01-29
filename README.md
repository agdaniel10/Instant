Bible Auto Display — Real-Time Verse Detection
Overview

Bible Auto Display is an offline, real-time system that automatically detects Bible verses spoken during a sermon and displays them on a screen within seconds. It uses speech-to-text transcription, regex pattern detection, and an offline Bible database to achieve near-instant verse display.

This prototype is designed for church automation, allowing staff to run a simple, offline application that displays scripture references as they are mentioned.

Features

Real-time transcription from your laptop microphone using Whisper (tiny/small models)

Regex-based detection of Bible verses (e.g., John 3:16, 1 Corinthians 13:4-7)

Offline Bible lookup from a JSON file (no internet required)

Immediate GUI display of detected verses

Fully offline and self-contained

Modular, production-ready folder structure for future expansions

Folder Structure
bible_auto_display/
├── main.py                  # Entry point: connects audio → transcription → detection → display
├── config.py                # Application configuration (mic, model, chunk size, etc.)
├── requirements.txt         # Python dependencies
├── bible/
│   ├── bible_data.json      # Bible text (book → chapter → verse)
│   └── lookup.py            # Lookup functions for Bible verses
├── audio/
│   └── mic_stream.py        # Handles microphone capture
├── transcription/
│   └── whisper_model.py     # Whisper model loading and transcription
├── detection/
│   └── regex_detector.py    # Regex logic to detect Bible verses
├── display/
│   └── gui_display.py       # GUI for displaying detected verses
└── utils/
    └── queue_helpers.py     # Utilities for thread-safe queues (optional)

Installation
1. Clone the repository
git clone <repository-url>
cd bible_auto_display

2. Install dependencies
pip install -r requirements.txt


Manual dependency installation (if not using requirements.txt):

pip install numpy
pip install pyaudio
pip install faster-whisper


Note: Tkinter is built-in for most Python distributions. On Linux, you may need to install it manually:

sudo apt install python3-tk


Windows PyAudio tip:

pip install pipwin
pipwin install pyaudio

Configuration

Edit config.py to adjust:

MIC_RATE = 16000         # Sampling rate
CHUNK_SIZE = 1024        # Audio buffer size
MODEL_SIZE = "small"     # Whisper model: tiny or small
LANGUAGE = "en"          # Language for transcription
BUFFER_SECONDS = 2       # Sliding window for verse detection

Usage

Ensure bible/bible_data.json exists and contains your Bible text in JSON format:

{
  "John": {"3": {"16": "For God so loved the world...", "17": "..."}},
  "Genesis": {"1": {"1": "In the beginning...", "2": "..."}}
}


Run the application:

python main.py


The GUI window will open:

Press Start (if you add controls later)

The system listens to your microphone, transcribes speech, detects Bible verses, and displays them immediately.

Press Ctrl+C in the terminal to stop.

How It Works

Audio Capture: Microphone input is captured in small chunks (~0.5–1s) using PyAudio.

Transcription: Audio chunks are transcribed in near real-time using Whisper (tiny or small models).

Verse Detection: Transcribed text is scanned with regex patterns to detect Bible references.

Lookup & Display: Detected verses are queried from an offline JSON Bible and displayed in the GUI immediately.

Future Improvements

Sliding buffer to handle partial verses across chunks

Voice Activity Detection to skip silence

Multi-threaded architecture to avoid GUI freezing

Support multiple Bible versions (e.g., KJV, NIV)

Web-based display for multiple screens/projectors

Logging & error handling for reliability in live church settings

Dependencies

Python 3.10+

numpy

pyaudio

faster-whisper

tkinter (built-in)

Optional (for GUI enhancements):

PyQt5 or PySide6

License

This project uses public domain Bible data (e.g., KJV). Ensure that any Bible version you include complies with copyright restrictions.

The code itself is released under MIT License, free to use and modify.

Acknowledgements

Faster Whisper
 for fast offline speech-to-text

Public domain Bible texts (e.g., KJV)
