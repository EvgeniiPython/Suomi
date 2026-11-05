# YouTube transcript to PDF

A self-contained GitHub Actions project that creates timestamped TXT, SRT and PDF transcripts from a public YouTube URL.

## How it works
1. Reads video metadata with yt-dlp.
2. Looks for creator-provided subtitles first, then YouTube auto-captions.
3. If no usable captions are available, downloads audio and transcribes it with faster-whisper on the GitHub-hosted runner (CPU, int8).
4. Writes transcript.txt, transcript.srt, transcript.pdf and metadata.json.
5. Uploads the files as a workflow artifact.

No paid transcription API is used. The first Whisper run downloads the selected model and can take a while.

## Target video
The initial video_url.txt points to:
https://youtu.be/GqiTxI9KbAQ

## Get the PDF
Open the Actions tab → YouTube transcript to PDF → the latest run → Artifacts → download youtube-transcript. The PDF is inside the downloaded ZIP.

## Run locally
Python 3.10+, FFmpeg and the packages in requirements.txt are required.

    python -m pip install -r requirements.txt
    python transcribe.py --url "https://youtu.be/GqiTxI9KbAQ" --output-dir output

For faster but less accurate fallback transcription, use --model base. The default is small.

## Choose a subtitle language
Optional:
    python transcribe.py --url "YOUTUBE_URL" --language en

When omitted, the script prefers the video's declared language, then the first available manual track, then the first auto-caption track.

## Notes
- The transcript is kept in the spoken language. No automatic translation is performed.
- Availability of captions/audio depends on YouTube access and video restrictions.
- If YouTube blocks the runner or the video is age/region restricted, the workflow will report the actual download error in the logs.
