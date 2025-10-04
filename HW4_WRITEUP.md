# HW4: Multimodal Agent with Speech Capabilities
## Jessica Wang - Harvard AI Studio

---

## Overview

This project extends the HW1/HW2 CrewAI agent system by adding **speech-to-text (STT)** and **text-to-speech (TTS)** capabilities, enabling voice-based interaction with the multi-agent system.

---

## Implementation Details

### Architecture

The voice interaction system follows this pipeline:

```
User Voice Input → Whisper STT → CrewAI Agent → Kokoro TTS → Audio Output
```

**Components:**

1. **Audio Recording** (`sounddevice` + `soundfile`)
   - Captures microphone input as WAV file
   - Configurable duration (default 8 seconds)
   - 16kHz sample rate for optimal Whisper performance

2. **Speech-to-Text** (`faster-whisper`)
   - Transcribes audio using OpenAI's Whisper model
   - Model sizes: tiny, base, small, medium, large-v3
   - Compute types: int8 (fast), float16, float32 (accurate)
   - Runs locally without API calls

3. **Agent Orchestration** (CrewAI)
   - Transcribed text passed as `user_prompt` input to crew
   - Two-agent pipeline: Profile Selector → Script Writer
   - Agents use knowledge source (resume PDF) to generate personalized intro
   - User voice input can modify tone/content preferences

4. **Text-to-Speech** (`kokoro-onnx` with system fallback)
   - Primary: Kokoro TTS (high-quality neural TTS)
   - Fallback: macOS `say` command (system TTS)
   - Outputs to `response.wav` and plays audio

### Libraries & APIs Used

| Component | Library | Purpose |
|-----------|---------|---------|
| STT | `faster-whisper` | Local Whisper inference (no API key needed) |
| TTS | `kokoro-onnx` | Neural text-to-speech synthesis |
| Audio I/O | `sounddevice`, `soundfile` | Recording and playback |
| Agent Framework | `crewai` | Multi-agent orchestration |
| LLM Backend | `openai` (via CrewAI) | GPT-3.5-turbo for agent reasoning |
| Environment | `python-dotenv` | Load API keys from `.env` |

### Key Code Changes

1. **`src/hw1/voice_cli.py`** (new)
   - Main voice interaction loop
   - Records audio, transcribes, runs crew, synthesizes speech
   - CLI with configurable parameters

2. **`src/hw1/main.py`**
   - Added `run_with_prompt(user_prompt)` function
   - Passes user input via `crew.kickoff(inputs={"user_prompt": ...})`

3. **`src/hw1/config/tasks.yaml`**
   - Injected `{user_prompt}` template variable into task descriptions
   - Allows voice input to influence agent behavior

4. **`pyproject.toml`**
   - Added `voice_cli` console script entry point

5. **`requirements.txt`**
   - Added: `faster-whisper`, `sounddevice`, `soundfile`, `kokoro-onnx`, `onnxruntime`

---

## Example Run

### Input (Voice)
**User speaks:** *"Make the intro a bit more casual and mention my love for machine learning."*

### Transcription (Whisper)
```
Transcript: Make the intro a bit more casual and mention my love for machine learning.
```

### Agent Processing (CrewAI)

**Agent 1: Profile Selector**
- Task: Extract relevant facts from Jessica's resume
- Output: Bullet outline with name, program, background, interests, fun detail

**Agent 2: Script Writer**
- Task: Convert outline into 2-3 sentence intro
- Input context: User's voice request for casual tone + ML emphasis
- Output:
```
Hi everyone, I'm Jessica! A Harvard M.S. Data Science candidate, 
with a passion for Machine Learning. I love coding in Python and 
building cool AI projects. Let's connect!
```

### Output (TTS)
- Text synthesized to speech via Kokoro TTS (or system fallback)
- Saved to `response.wav`
- Played through speakers

---

## Insights & Observations

### 1. **Latency Breakdown**
- **Recording**: ~3-8 seconds (user-controlled)
- **Whisper transcription**: ~2-5 seconds (depends on model size)
- **CrewAI execution**: ~10-20 seconds (LLM API calls, knowledge retrieval)
- **TTS synthesis**: ~1-2 seconds
- **Total**: ~20-35 seconds for full voice interaction

### 2. **Accuracy & Quality**
- **Whisper STT**: Excellent accuracy even with `tiny` model for clear speech
- **Agent understanding**: Successfully interprets voice requests (tone, content preferences)
- **TTS quality**: Kokoro provides natural-sounding speech (when configured); system TTS is functional fallback

### 3. **Design Trade-offs**
- **Local vs Cloud**: Whisper runs locally (privacy + no API costs) but requires compute
- **Model size**: `tiny` is fast but less accurate; `small` is good balance; `large-v3` is most accurate but slow
- **Compute type**: `int8` quantization speeds up inference with minimal quality loss

### 4. **User Experience**
- Voice input feels natural for quick requests
- Waiting for agent response can feel long (consider streaming in future)
- Audio feedback confirms system is working (recording, transcribing, etc.)

### 5. **Challenges**
- **Kokoro setup**: Requires downloading voice models separately (not pip-installable)
- **Environment variables**: Need to load `.env` explicitly in CLI context
- **Audio permissions**: macOS requires microphone access approval

---

## Running the System

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install package in editable mode (for console scripts)
pip install -e .

# Ensure .env has OPENAI_API_KEY
echo "OPENAI_API_KEY=sk-..." > .env
```

### Usage
```bash
# Basic usage (8 seconds, small model, Kokoro TTS)
voice_cli --duration 8 --model small --compute_type int8 --voice af_bella

# Quick test (3 seconds, tiny model, system TTS fallback)
voice_cli --duration 3 --model tiny --use_system_tts

# High accuracy (10 seconds, large model)
voice_cli --duration 10 --model large-v3 --compute_type float16 --use_system_tts
```

### Parameters
- `--duration`: Recording length in seconds (default: 8)
- `--model`: Whisper model size (`tiny`, `base`, `small`, `medium`, `large-v3`)
- `--compute_type`: Inference precision (`int8`, `float16`, `float32`)
- `--voice`: Kokoro voice ID (e.g., `af_bella`)
- `--use_system_tts`: Use macOS `say` command as TTS fallback
- `--no_playback`: Save audio but don't play it

---

## Future Enhancements

1. **Voice Activity Detection (VAD)**: Auto-stop recording when user finishes speaking
2. **Streaming TTS**: Start playback before full synthesis completes
3. **Conversation history**: Multi-turn voice dialogue
4. **Interrupt handling**: Allow user to interrupt agent mid-response
5. **Cloud TTS options**: Add OpenAI TTS, ElevenLabs as alternatives
6. **Mobile/web interface**: Extend beyond CLI

---

## Deliverables

✅ **GitHub Repo**: Extended code with voice capabilities  
✅ **Video Demo**: Unlisted YouTube link showing voice interaction  
✅ **Write-up**: This document (implementation + example run + insights)

---

## Conclusion

Adding voice capabilities transforms the agent from a text-based tool into a more natural, conversational interface. The combination of local Whisper STT and neural TTS creates a responsive system that maintains privacy while delivering high-quality voice interaction. The modular design allows easy swapping of STT/TTS backends and scales to more complex multi-agent workflows.

**Key Takeaway**: Voice interfaces require careful orchestration of multiple components (audio I/O, transcription, agent logic, synthesis) with attention to latency, accuracy, and user feedback at each stage.
