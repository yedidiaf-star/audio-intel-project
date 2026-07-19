
"""Task 06 - window segmentation and speaker consolidation.

Slides a window across the audio, asks task 05 who is speaking in each
window, then merges neighbouring windows that share a speaker into one
continuous segment. Output matches the shared API contract:

    {"segments": [{"start", "end", "speaker", "confidence"}, ...]}
"""

from __future__ import annotations

import tempfile
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

from pydub import AudioSegment

from tasks.task_05_identification import identify_single_segment


@dataclass(frozen=True)
class WindowConfig:
    """How the audio is sliced before each window is identified."""

    window_seconds: float = 2.25
    hop_seconds: float = 0.75  # smaller than window_seconds => windows overlap

    @property
    def window_ms(self) -> int:
        return int(self.window_seconds * 1000)

    @property
    def hop_ms(self) -> int:
        return int(self.hop_seconds * 1000)


@dataclass
class WindowResult:
    """One window's identification, in seconds."""

    start: float
    end: float
    speaker: str
    confidence: float

@dataclass
class Segment:
    """Consecutive same-speaker windows merged into a single span."""

    start: float
    end: float
    speaker: str
    confidences: list[float] = field(default_factory=list)

    @property
    def confidence(self) -> float:
        """Mean confidence across the merged windows."""
        return round(sum(self.confidences) / len(self.confidences), 2)

    def to_dict(self) -> dict:
        return {
            "start": round(self.start, 2),
            "end": round(self.end, 2),
            "speaker": self.speaker,
            "confidence": self.confidence,
        }

@contextmanager
def _window_clip(audio: AudioSegment, *, start_ms: int, end_ms: int):
    """Write one slice of audio to a temp .wav and yield its path.

    task 05 identifies speakers from a file path, so each window has to
    live on disk for the length of that call. The file is removed after.
    """
    clip = audio[start_ms:end_ms]
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    try:
        clip.export(tmp.name, format="wav")
        tmp.close()
        yield tmp.name
    finally:
        Path(tmp.name).unlink(missing_ok=True)

def _iter_windows(total_ms: int, config: WindowConfig):
    """Yield (start_ms, end_ms) window bounds across the whole clip."""
    start_ms = 0
    while start_ms < total_ms:
        end_ms = min(start_ms + config.window_ms, total_ms)
        yield start_ms, end_ms
        if end_ms >= total_ms:  # last window already reached the end
            break
        start_ms += config.hop_ms

def _identify_windows(audio: AudioSegment, config: WindowConfig) -> list[WindowResult]:
    """Run task 05 on every window and collect the raw per-window results."""
    results: list[WindowResult] = []
    for start_ms, end_ms in _iter_windows(len(audio), config=config):
        with _window_clip(audio, start_ms=start_ms, end_ms=end_ms) as clip_path:
            identified = identify_single_segment(clip_path)
        results.append(
            WindowResult(
                start=start_ms / 1000.0,
                end=end_ms / 1000.0,
                speaker=identified["speaker"],
                confidence=identified["confidence"],
            )
        )
    return results

def _consolidate(windows: list[WindowResult]) -> list[Segment]:
    """Merge neighbouring windows that share a speaker into one segment."""
    segments: list[Segment] = []
    for window in windows:
        current = segments[-1] if segments else None
        if current is not None and current.speaker == window.speaker:
            current.end = window.end
            current.confidences.append(window.confidence)
        else:
            segments.append(
                Segment(
                    start=window.start,
                    end=window.end,
                    speaker=window.speaker,
                    confidences=[window.confidence],
                )
            )
    return segments

def _make_contiguous(segments: list[Segment]) -> list[Segment]:
    """Snap shared boundaries so the timeline is one clean partition.

    Overlapping windows leave neighbouring segments overlapping too; splitting
    at the midpoint gives each boundary a single, non-overlapping value. With
    non-overlapping windows this is a no-op.
    """
    for earlier, later in zip(segments, segments[1:]):
        boundary = round((earlier.end + later.start) / 2, 2)
        earlier.end = boundary
        later.start = boundary
    return segments

def segment_and_identify(file_url, config: WindowConfig | None = None):
    """Segment `file_url` by speaker and return the consolidated timeline.

    `config` is optional, so the original one-argument call still works.
    """
    config = config or WindowConfig()
    audio = AudioSegment.from_file(file_url)

    windows = _identify_windows(audio, config=config)
    segments = _consolidate(windows)
    segments = _make_contiguous(segments)

    return {"segments": [segment.to_dict() for segment in segments]}