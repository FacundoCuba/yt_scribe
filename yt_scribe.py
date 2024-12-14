import os
import whisper
import torch
from yt_dlp import YoutubeDL
import warnings
import argparse
import json

# Suppress PyTorch FutureWarning
warnings.filterwarnings("ignore", category=FutureWarning)

# Function to download audio and get video metadata
def download_audio(youtube_url, output_file="audio.mp3"):
    """Download audio from a YouTube video and return metadata."""
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': output_file,
        'quiet': False
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=True)
            metadata = {
                "title": info.get('title', 'transcription').replace(" ", "_").replace("/", "_"),
                "channel": info.get('channel', 'Unknown Channel'),
                "publish_date": info.get('upload_date', 'Unknown Date'),
            }
        print(f"Audio downloaded successfully: {output_file}")
        return output_file, metadata
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None, None

# Function to transcribe audio using Whisper with GPU support
def transcribe_audio(audio_file, output_text_file, model_size="base", language=None):
    """Transcribe audio using Whisper with GPU support."""
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {device.upper()}")

        model = whisper.load_model(model_size).to(device)
        print(f"Transcribing audio using model: {model_size}...")

        result = model.transcribe(audio_file, language=language)
        detected_language = result['language'] if language is None else language
        with open(output_text_file, "w", encoding="utf-8") as file:
            file.write(result['text'])

        print(f"Transcription saved to: {output_text_file}")
        return result['text'], detected_language
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None, None

# Main function
def main():
    parser = argparse.ArgumentParser(
        description="YouTube Audio Transcription Script",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("-u", "--urls", help="Comma-separated YouTube URLs or a file path", required=True)
    parser.add_argument("-o", "--output_dir", help="Output directory", default=".")
    parser.add_argument("-m", "--model_size", help="Whisper model size (tiny, base, small, medium, large)", default="base")
    parser.add_argument("-l", "--language", help="Language code (e.g., 'en' for English, 'es' for Spanish)", default=None)
    args = parser.parse_args()

    if not args.urls:
        print("Error: No URLs or file path provided. Use --help for usage information.")
        return

    if os.path.isfile(args.urls):
        try:
            with open(args.urls, "r", encoding="utf-8") as file:
                youtube_urls = [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            print("File not found. Exiting.")
            return
    else:
        youtube_urls = [url.strip() for url in args.urls.split(",")]

    # Process each YouTube URL
    for youtube_url in youtube_urls:
        print(f"\nProcessing: {youtube_url}")

        # Step 1: Download audio
        output_audio = "audio.mp3"
        audio_file, metadata = download_audio(youtube_url, output_file=output_audio)
        if not audio_file or not metadata:
            print("Failed to download audio. Skipping.")
            continue

        # Set file paths
        video_title = metadata['title']
        output_text_file = os.path.join(args.output_dir, f"{video_title}_transcription.txt")
        output_metadata_file = os.path.join(args.output_dir, f"{video_title}_metadata.json")

        # Step 2: Transcribe audio
        transcription, detected_language = transcribe_audio(audio_file, output_text_file, model_size=args.model_size, language=args.language)
        if not transcription:
            print("Failed to transcribe audio. Skipping.")
            continue

        # Save metadata
        metadata['detected_language'] = detected_language
        with open(output_metadata_file, "w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=4)
        print(f"Metadata saved to: {output_metadata_file}")

        # Step 3: Clean up
        if os.path.exists(output_audio):
            os.remove(output_audio)
            print(f"Temporary audio file removed: {output_audio}")

    print("\nProcess completed successfully.")

if __name__ == "__main__":
    main()

