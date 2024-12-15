# YouTube Audio Transcription Script

## Overview
`yt_scribe.py` is a command-line tool that downloads audio from YouTube videos, transcribes the audio using OpenAI's Whisper model, and exports both the transcription and relevant metadata as files.

## Features
- **Audio Download:** Extracts audio from YouTube videos.
- **Automatic Transcription:** Transcribes audio using Whisper with GPU/CPU support.
- **Language Auto-Detection:** Detects language automatically if not specified.
- **Metadata Export:** Saves video metadata (title, channel, publish date, and detected language) to a JSON file.
- **Customizable Output:** Configurable model size, language, and output directory.

## Requirements
- Python 3.8+
- Libraries:
  - `torch`
  - `whisper`
  - `yt-dlp`
  - `argparse`
  - `json`

## Installation
### Using Conda Environment
1. Create and activate a Conda environment:
   ```bash
   conda create -n yt_scribe_env python=3.8 -y
   conda activate yt_scribe_env
   ```
2. Install dependencies:
   ```bash
   pip install torch whisper yt-dlp
   ```

### Manual Installation
1. Download the script.
2. Install dependencies:
   ```bash
   pip install torch whisper yt-dlp
   ```

## Usage
### Basic Command:
```bash
python yt_scribe.py -u "<YouTube_URL>" -o <output_directory>
```

### Command-Line Arguments:
| Argument              | Description                                         | Default         |
|----------------------|-----------------------------------------------------|-----------------|
| `-u`, `--urls`       | Comma-separated YouTube URLs or file path          | Required        |
| `-o`, `--output_dir` | Output directory                                    | Current directory |
| `-m`, `--model_size` | Whisper model size (`tiny`, `base`, `small`, `medium`, `large`) | `base`          |
| `-l`, `--language`   | Language code (e.g., `en`, `es`) or auto-detection | Auto-detect    |

### Example:
```bash
python yt_scribe.py -u "https://www.youtube.com/watch?v=dQw4w9WgXcQ" -o transcriptions/ -m base -l en
```

### Processing a List of URLs:
```bash
python yt_scribe.py -u youtube_urls.txt -o transcriptions/
```

## Output Files
1. **Transcription File:** `<video_title>_transcription.txt`
2. **Metadata File:** `<video_title>_metadata.json`

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contact
For any questions, reach out at my [mail](mailto:facundogcuba@gmail.com).
