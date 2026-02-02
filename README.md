# Subtitles Generator

This program automatically creates subtitle files (`.srt`) from video or audio files. It uses the Whisper AI model to generate the text.

---

## How to Use (for Windows Users)

Follow these steps to generate subtitles.

### Step 1: Place Media Files

1.  Open the folder named `input_files`.
2.  Copy and paste video or audio files into this folder.

    *Example:*
    ```
    Subtitle_Generator_Tool/
    │
    └─── input_files/
         ├── my_video_01.mp4
         └─── my_other_audio_file.wav
    ```

### Step 2: Check the Configuration File (Optional)

The program's settings can be changed by editing the `CONFIG.json` file. This file can be opened with a text editor like Notepad. Or it can also be edited in any editor (code editor like PyCharm is also fine).

```json
{
  "language": "en",
  "model_size": "small",
  "device": "cpu",
  "output_format": "srt",
  "input_extensions": [".mp4", ".mov", ".wav", ".m4a", ".mkv"]
}
```

**Explanation of Settings:**

*   **`"model_size"`**: This controls the quality and speed.
    *   `"small"`: Faster, good quality. (Recommended)
    *   `"medium"`: Slower, slightly better quality. The computer may become very slow when using this.
    *   `"base"`: Fastest, but lower quality.
    * `"large"` or `"turbo"` : not recommended for normal machines. Only try this if a lot of time can be spared as this will be painfully slow with a normal CPU.

*   **`"language"`**: The language spoken in the media file. `"en"` is for English. (not sure about support for other languages)

*   **`"output_format"`**: The format of the subtitle file. `"srt"` is a standard format that works with most video editors like DaVinci Resolve. Only `.srt` format is supported for now.

### Step 3: Run the Program

1.  Return to the main folder.
2.  Double-click the file named `RUN_ME.bat`.

A black window will appear. This is normal.

*   **First Time Use:** The first time the program runs, it will download the AI model. This can take a few minutes.
*   **During Processing:** The program will start processing the files. The computer's fan may become loud. This is also normal. The process can take a long time, depending on the length of the media files.

### Step 4: Find The Subtitle Files

Once the program is finished, a "Press any key to continue..." message will be visible in the black window.

1.  Open the folder named `output_files`.
2.  The new subtitle files will be inside this folder. They will have the same name as the original files, but with a `.srt` extension.

    *Example:*
    ```
    Subtitle_Generator_Tool/
    │
    └─── output_files/
         ├── my_video_01.srt
         └─── my_audio_file.srt
    ```

These `.srt` files can now be imported into video editing software.

---

## How to Use (for macOS Users)
This program assumes `ffmpeg` is installed in the system. If it is not installed. Install this with `brew install ffmepg`.

1.  Place video or audio files in the `input_files` folder.
2.  (Optional) Edit the `CONFIG.json` file to change settings.
3.  Open the Terminal application.
4.  Drag the `RUN_ME.sh` file into the Terminal window and press Enter.
5.  Find the finished subtitle files in the `output_files` folder.

---

## Technical Overview

### Features

*   **Automatic Transcription:** Transcribes audio from various video/audio formats into text.
*   **Subtitle Generation:** Creates `.srt` subtitle files with accurate timestamps.
*   **CPU Optimized:** Uses `faster-whisper` with `int8` quantization for efficient performance on standard CPUs.
*   **Cross-Platform:** Designed to run on both Windows and macOS.
*   **Self-Contained Dependencies:** Includes a batch script to create a local Python virtual environment (`.venv`) and install all necessary libraries.
*   **Portable FFmpeg (Windows):** Bundles `ffmpeg.exe` for audio extraction on Windows, so no system-wide installation is needed.

### Project Structure

```plaintext
Subtitle_Generator_Tool/
│
├── input_files/            # Folder for input media files.
├── output_files/           # Folder for the generated subtitle files.
├── tools/                  # Contains the ffmpeg.exe for Windows.
│   └── ffmpeg.exe
│
├── src/                    # Source code for the application.
│   ├── __init__.py
│   ├── transcriber.py      # Core logic for audio extraction and transcription.
│   └── utils.py            # Helper functions (e.g., timestamp formatting).
│
├── CONFIG.json             # Configuration file for settings.
├── requirements.txt        # Python dependencies.
├── main.py                 # Main entry point of the script.
├── RUN_ME.bat              # Setup and execution script for Windows.
└── RUN_ME.sh               # Setup and execution script for macOS/Linux.
```

### Developer Setup

1.  **Clone the repository.**
2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```
3.  **Activate the environment:**
    *   Windows: `.venv\Scripts\activate`
    *   macOS/Linux: `source .venv/bin/activate`
4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Run the script:**
    ```bash
    python main.py
    ```
6.  **FFmpeg Prerequisite (macOS/Linux):** Ensure FFmpeg is installed and available in the system's PATH. It can be installed via Homebrew: `brew install ffmpeg`.
