import argparse
import os
import sys
import tempfile
from typing import Optional

import numpy as np
import sounddevice as sd
import soundfile as sf
from dotenv import load_dotenv

from faster_whisper import WhisperModel

# Load environment variables from .env file
load_dotenv()

# Ensure we can import the crew runner
sys.path.append(os.path.join(os.path.dirname(__file__), "."))
from hw1.main import run_with_prompt


def record_audio(outfile: str, duration: float = 8.0, samplerate: int = 16000, channels: int = 1):
    print(f"Recording {duration:.1f}s of audio. Speak now...", flush=True)
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype="float32")
    sd.wait()
    sf.write(outfile, audio, samplerate)
    print(f"Saved recording to {outfile}", flush=True)


def transcribe(audio_path: str, model_size: str = "small", compute_type: str = "int8") -> str:
    print("Transcribing with Faster-Whisper...", flush=True)
    model = WhisperModel(model_size, device="auto", compute_type=compute_type)
    segments, info = model.transcribe(audio_path, beam_size=1)
    text_parts = []
    for seg in segments:
        text_parts.append(seg.text)
    transcript = " ".join(t.strip() for t in text_parts).strip()
    print(f"Transcript: {transcript}", flush=True)
    return transcript


def _kokoro_generate_audio(text: str, voice: str = "af_bella") -> Optional[tuple[np.ndarray, int]]:
    """
    Synthesize speech using Kokoro TTS (KPipeline).
    Returns (waveform, sample_rate) if successful, otherwise None.
    """
    try:
        from kokoro import KPipeline  # type: ignore
        
        # Initialize pipeline with American English ('a' lang code)
        pipeline = KPipeline(lang_code='a')
        
        # Generate audio - returns generator of (graphemes, phonemes, audio)
        generator = pipeline(text, voice=voice)
        
        # Collect all audio chunks
        audio_chunks = []
        for _, _, audio in generator:
            audio_chunks.append(audio)
        
        if not audio_chunks:
            print("Kokoro generated no audio chunks.", flush=True)
            return None
        
        # Concatenate all chunks
        full_audio = np.concatenate(audio_chunks)
        return (full_audio, 24000)  # Kokoro outputs at 24kHz
        
    except ImportError as e:
        print("Kokoro TTS not installed. Install with: pip install kokoro>=0.9.4", flush=True)
        print("Also ensure espeak-ng is installed (brew install espeak-ng on macOS)", flush=True)
        print(f"Error: {e}", flush=True)
        return None
    except Exception as e:
        print("Kokoro TTS failed to run.", flush=True)
        print(f"Error: {e}", flush=True)
        print("Ensure espeak-ng is installed: brew install espeak-ng", flush=True)
        return None


def speak_with_kokoro(text: str, out_wav: str = "response.wav", voice: str = "af_bella") -> bool:
    result = _kokoro_generate_audio(text, voice=voice)
    if result is None:
        return False
    
    wav, sr = result
    wav = np.asarray(wav, dtype=np.float32)
    
    # Normalize if needed
    max_abs = np.max(np.abs(wav)) if wav.size > 0 else 1.0
    if max_abs > 1.0:
        wav = wav / max_abs
    
    sf.write(out_wav, wav, sr)
    print(f"Saved TTS audio to {out_wav}", flush=True)
    return True


def play_wav(path: str):
    data, sr = sf.read(path, dtype='float32')
    print("Playing audio...", flush=True)
    sd.play(data, sr)
    sd.wait()


def main():
    parser = argparse.ArgumentParser(description="Voice CLI: Whisper STT -> CrewAI -> Kokoro TTS")
    parser.add_argument("--duration", type=float, default=8.0, help="Recording duration in seconds")
    parser.add_argument("--model", type=str, default="small", help="Faster-Whisper model size (e.g., tiny, base, small, medium, large-v3)")
    parser.add_argument("--compute_type", type=str, default="int8", help="Faster-Whisper compute type (e.g., int8, float16, float32)")
    parser.add_argument("--voice", type=str, default="af_bella", help="Kokoro voice ID")
    parser.add_argument("--no_playback", action="store_true", help="Do not play TTS audio, only save file")
    parser.add_argument("--use_system_tts", action="store_true", help="Use system TTS (macOS 'say') as fallback")

    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmpdir:
        in_wav = os.path.join(tmpdir, "input.wav")
        record_audio(in_wav, duration=args.duration)
        text = transcribe(in_wav, model_size=args.model, compute_type=args.compute_type)

    # Run Crew with the transcribed text
    response = run_with_prompt(text)

    # TTS
    out_wav = os.path.abspath("response.wav")
    ok = speak_with_kokoro(response, out_wav=out_wav, voice=args.voice)
    
    if not ok and args.use_system_tts:
        # Fallback to system TTS on macOS
        print("Using system TTS as fallback...", flush=True)
        import subprocess
        subprocess.run(["say", response])
    elif ok and not args.no_playback:
        play_wav(out_wav)


if __name__ == "__main__":
    main()
