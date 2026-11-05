#!/usr/bin/env python3
"""Download YouTube subtitles, falling back to local Whisper transcription, and build PDF/TXT/SRT."""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


@dataclass
class Segment:
    start: float
    end: float
    text: str


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(str(x) for x in cmd), flush=True)
    result = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.stdout.strip():
        print(result.stdout[-4000:], flush=True)
    if result.returncode != 0:
        message = result.stderr.strip()[-6000:]
        if check:
            raise RuntimeError(
                f"Command failed ({result.returncode}): {' '.join(cmd)}\n{message}"
            )
        print(message, file=sys.stderr, flush=True)
    return result


def timestamp_to_seconds(value: str) -> float:
    value = value.strip().replace(",", ".")
    parts = value.split(":")
    if len(parts) == 3:
        hours, minutes, seconds = parts
    elif len(parts) == 2:
        hours, minutes, seconds = "0", parts[0], parts[1]
    else:
        raise ValueError(f"Unsupported timestamp: {value}")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)


def clean_caption_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value)
    value = value.replace("\\N", " ").replace("\\n", " ")
    return re.sub(r"\s+", " ", value).strip()


def parse_caption_file(path: Path) -> list[Segment]:
    content = path.read_text(encoding="utf-8-sig", errors="replace")
    lines = content.splitlines()
    segments: list[Segment] = []
    i = 0
    time_re = re.compile(
        r"(?P<start>(?:\d+:)?\d{2}:\d{2}[,.]\d{3})\s*-->\s*"
        r"(?P<end>(?:\d+:)?\d{2}:\d{2}[,.]\d{3})"
    )
    while i < len(lines):
        match = time_re.search(lines[i])
        if not match:
            i += 1
            continue
        start = timestamp_to_seconds(match.group("start"))
        end = timestamp_to_seconds(match.group("end"))
        i += 1
        text_lines: list[str] = []
        while i < len(lines) and lines[i].strip():
            line = lines[i].strip()
            if line.upper().startswith(("NOTE", "STYLE", "REGION")):
                break
            text_lines.append(line)
            i += 1
        text = clean_caption_text(" ".join(text_lines))
        if text and not text.startswith(("[音楽]", "[музыка]")):
            if not segments or text != segments[-1].text:
                segments.append(Segment(start, max(end, start + 0.05), text))
        i += 1
    return segments


def track_language(info: dict, requested: str | None) -> tuple[str | None, bool]:
    manual = info.get("subtitles") or {}
    automatic = info.get("automatic_captions") or {}
    all_languages = list(manual) + [x for x in automatic if x not in manual]
    if not all_languages:
        return None, False

    preferred = requested or info.get("language")
    chosen = None
    if preferred:
        if preferred in all_languages:
            chosen = preferred
        else:
            chosen = next(
                (code for code in all_languages if code.lower().split("-")[0] == preferred.lower().split("-")[0]),
                None,
            )
    if chosen is None and manual:
        chosen = next(iter(manual))
    if chosen is None:
        chosen = next(iter(automatic))
    return chosen, chosen not in manual


def download_video_info(url: str) -> dict:
    result = run([
        sys.executable, "-m", "yt_dlp", "--dump-single-json",
        "--skip-download", "--no-warnings", url
    ])
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("yt-dlp did not return valid video metadata.") from exc


def obtain_captions(
    url: str, info: dict, work_dir: Path, requested_language: str | None
) -> tuple[list[Segment], str] | None:
    language, is_auto = track_language(info, requested_language)
    if not language:
        print("No subtitle tracks are advertised by YouTube.", flush=True)
        return None

    subtitle_dir = work_dir / "subtitles"
    subtitle_dir.mkdir(parents=True, exist_ok=True)
    flag = "--write-auto-subs" if is_auto else "--write-subs"
    run(
        [
            sys.executable, "-m", "yt_dlp",
            "--skip-download", "--no-warnings",
            flag, "--sub-langs", language,
            "--sub-format", "vtt/best",
            "--convert-subs", "vtt",
            "-o", str(subtitle_dir / "caption.%(ext)s"),
            url,
        ],
        check=False,
    )
    candidates = sorted(
        p for p in subtitle_dir.glob("*")
        if p.suffix.lower() in {".vtt", ".srt"}
    )
    if not candidates:
        print("Subtitle track could not be downloaded or converted; using speech recognition.", flush=True)
        return None

    chosen = candidates[0]
    segments = parse_caption_file(chosen)
    if not segments:
        print(f"Subtitle file {chosen.name} contained no usable cues; using speech recognition.", flush=True)
        return None
    label = f"{'auto-captions' if is_auto else 'manual subtitles'} ({language})"
    return segments, label


def transcribe_audio(url: str, work_dir: Path, model_size: str) -> tuple[list[Segment], str]:
    audio_dir = work_dir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    output_template = str(audio_dir / "source.%(ext)s")
    run([
        sys.executable, "-m", "yt_dlp",
        "-f", "bestaudio/best", "-o", output_template,
        "--no-playlist", "--no-warnings", url,
    ])
    audio_files = [
        p for p in audio_dir.iterdir()
        if p.is_file() and p.suffix.lower() not in {".part", ".json"}
    ]
    if not audio_files:
        raise RuntimeError("yt-dlp finished without producing an audio file.")
    source_audio = max(audio_files, key=lambda p: p.stat().st_size)
    wav_path = audio_dir / "audio_16khz_mono.wav"
    run([
        "ffmpeg", "-y", "-i", str(source_audio), "-vn",
        "-ac", "1", "-ar", "16000", str(wav_path)
    ])

    print(f"Loading faster-whisper model: {model_size} (CPU / int8)", flush=True)
    from faster_whisper import WhisperModel

    model = WhisperModel(model_size, device="cpu", compute_type="int8", cpu_threads=2, num_workers=1)
    whisper_segments, detected = model.transcribe(
        str(wav_path), beam_size=5, vad_filter=True, condition_on_previous_text=True
    )
    segments = [
        Segment(float(item.start), float(item.end), clean_caption_text(item.text))
        for item in whisper_segments
        if clean_caption_text(item.text)
    ]
    if not segments:
        raise RuntimeError("Speech recognition completed but returned no text.")
    return segments, f"faster-whisper {model_size}; detected language: {detected.language}"


def format_time(seconds: float, srt: bool = False) -> str:
    milliseconds = max(0, int(round(seconds * 1000)))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    separator = "," if srt else "."
    return f"{hours:02}:{minutes:02}:{secs:02}{separator}{ms:03}"


def write_text_and_srt(segments: list[Segment], output_dir: Path, title: str, source: str) -> None:
    header = f"{title}\nSource: {source}\n\n"
    txt = header + "\n".join(
        f"[{format_time(s.start)}] {s.text}" for s in segments
    )
    (output_dir / "transcript.txt").write_text(txt + "\n", encoding="utf-8")

    blocks = []
    for number, segment in enumerate(segments, 1):
        blocks.append(
            f"{number}\n{format_time(segment.start, True)} --> "
            f"{format_time(segment.end, True)}\n{segment.text}\n"
        )
    (output_dir / "transcript.srt").write_text("\n".join(blocks), encoding="utf-8")


def register_unicode_fonts() -> tuple[str, str]:
    candidates = [
        (
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ),
        (
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
        ),
    ]
    for regular, bold in candidates:
        if Path(regular).exists() and Path(bold).exists():
            pdfmetrics.registerFont(TTFont("TranscriptSans", regular))
            pdfmetrics.registerFont(TTFont("TranscriptSans-Bold", bold))
            return "TranscriptSans", "TranscriptSans-Bold"
    raise RuntimeError("No Unicode font found. Install fonts-dejavu-core or fonts-noto-core.")


def create_pdf(
    segments: list[Segment], path: Path, title: str, source: str, url: str
) -> None:
    regular_font, bold_font = register_unicode_fonts()
    doc = SimpleDocTemplate(
        str(path), pagesize=A4,
        rightMargin=18 * mm, leftMargin=18 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
        title=f"Transcript — {title}",
        author="YouTube Transcript PDF workflow",
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TranscriptTitle", parent=styles["Title"], fontName=bold_font,
        fontSize=17, leading=22, alignment=TA_CENTER, spaceAfter=8,
    )
    meta_style = ParagraphStyle(
        "TranscriptMeta", parent=styles["Normal"], fontName=regular_font,
        fontSize=8, leading=11, textColor=colors.HexColor("#555555"), spaceAfter=3,
    )
    body_style = ParagraphStyle(
        "TranscriptBody", parent=styles["BodyText"], fontName=regular_font,
        fontSize=9, leading=13, spaceAfter=6, splitLongWords=1,
    )
    story = [
        Paragraph(html.escape(title), title_style),
        Paragraph(f"<b>Source:</b> {html.escape(source)}", meta_style),
        Paragraph(f"<b>Video:</b> {html.escape(url)}", meta_style),
        Paragraph(f"<b>Transcript entries:</b> {len(segments)}", meta_style),
        Spacer(1, 8),
    ]
    for segment in segments:
        stamp = format_time(segment.start)
        body = html.escape(segment.text).replace("\n", "<br/>")
        story.append(Paragraph(f'<font name="{bold_font}">{stamp}</font>  {body}', body_style))

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont(regular_font, 8)
        canvas.setFillColor(colors.HexColor("#777777"))
        canvas.drawString(18 * mm, 10 * mm, "YouTube transcript")
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {document.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=None, help="Public YouTube URL; defaults to VIDEO_URL or video_url.txt")
    parser.add_argument("--language", default=None, help="Preferred subtitle language code, e.g. en or ru")
    parser.add_argument("--model", default="small", help="faster-whisper fallback model (tiny, base, small, medium)")
    parser.add_argument("--output-dir", type=Path, default=Path("output"))
    args = parser.parse_args()

    url = args.url or os.environ.get("VIDEO_URL")
    if not url and Path("video_url.txt").exists():
        url = Path("video_url.txt").read_text(encoding="utf-8").strip()
    if not url:
        parser.error("Provide --url, set VIDEO_URL or put the URL in video_url.txt.")

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    work_dir = Path("work")
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir(parents=True)

    info = download_video_info(url)
    title = info.get("title") or info.get("id") or "YouTube video"
    print(f"Video: {title}", flush=True)
    result = obtain_captions(url, info, work_dir, args.language)
    if result is None:
        segments, source = transcribe_audio(url, work_dir, args.model)
    else:
        segments, source = result

    write_text_and_srt(segments, output_dir, title, source)
    create_pdf(segments, output_dir / "transcript.pdf", title, source, url)
    metadata = {
        "url": url,
        "video_id": info.get("id"),
        "title": title,
        "duration_seconds": info.get("duration"),
        "upload_date": info.get("upload_date"),
        "source": source,
        "language": info.get("language"),
        "entries": len(segments),
        "method": "captions" if "subtitles" in source or "auto-captions" in source else "speech_recognition",
    }
    (output_dir / "metadata.json").write_text(
        json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"SUCCESS: {len(segments)} entries written to {output_dir.resolve()}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr, flush=True)
        raise SystemExit(1)
