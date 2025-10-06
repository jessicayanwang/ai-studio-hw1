# Multimodal Agent with Speech Capabilities
**Jessica Wang**

---

## Implementation: Voice Interaction System

For this assignment, I extended my existing CrewAI multi-agent system (from HW1/HW2g) by adding speech-to-text (STT) and text-to-speech (TTS) capabilities. This allows users to interact with the agent through voice rather than text, creating a more natural conversational interface.

### Architecture Overview

I implemented a pipeline that flows as follows: **User Voice Input → Whisper STT → CrewAI Agent → Kokoro TTS → Audio Output**. Each component was chosen to balance quality, latency, and ease of deployment.

### Libraries and Implementation Details

**Speech-to-Text (Whisper):** I used `faster-whisper`, a Python library that provides local inference for OpenAI's Whisper model. I chose this over the cloud-based Whisper API because it runs entirely locally, which means no API costs, better privacy, and no network dependency. The library supports multiple model sizes (tiny, base, small, medium, large-v3) and compute types (int8, float16, float32). For my implementation, I used the `small` model with `int8` quantization, which provides a good balance between accuracy and speed (~2-4 seconds transcription time).

**Audio Recording:** I used `sounddevice` and `soundfile` to capture microphone input and save it as a WAV file. I configured the recording at 16kHz sample rate, which is optimal for Whisper's performance. The recording duration is configurable (default 8 seconds), giving users enough time to speak their request.

**Agent Orchestration:** My existing CrewAI system consists of two agents: a Profile Selector that extracts relevant facts from my resume (stored as a PDF knowledge source), and a Script Writer that generates a personalized introduction. To integrate voice input, I modified the task configuration files (`src/hw1/config/tasks.yaml`) to accept a `{user_prompt}` template variable. This allows the transcribed speech to influence the agent's behavior—for example, if the user requests a "casual tone" or asks to "mention machine learning," the agents incorporate these preferences into their output.

**Text-to-Speech (Kokoro):** For TTS, I used Kokoro (version 0.9.4+), an open-source neural TTS model based on StyleTTS2 architecture. Kokoro requires `espeak-ng` as a system dependency for phonemization (converting text to phonemes). I implemented the TTS using Kokoro's `KPipeline` API, which returns a generator that yields audio chunks. I concatenate these chunks and save the result as a 24kHz WAV file. The model downloads automatically (~327MB) on first run from HuggingFace. As a fallback, I also added support for macOS's built-in `say` command in case Kokoro setup fails.

**Integration:** I created a new CLI tool (`src/hw1/voice_cli.py`) that orchestrates the entire pipeline. The CLI uses `python-dotenv` to load environment variables (like the OpenAI API key needed by CrewAI), records audio, transcribes it, passes the transcript to the agent via `crew.kickoff(inputs={"user_prompt": ...})`, synthesizes the response with Kokoro, and plays the audio back through the speakers.

### Technical Challenges

I encountered a few technical challenges during implementation:

1. **NumPy Compatibility:** Kokoro's dependencies (scipy, transformers) require `numpy<2.0`, but some other packages had installed numpy 2.3.3. I had to downgrade numpy to resolve import errors.

2. **Model Loading:** Both Whisper and Kokoro load their models fresh on every run, which adds ~3-5 seconds of overhead. For a production system, I would implement model caching or a persistent server to keep models in memory.

3. **Environment Variables:** When running the CLI as a standalone script, the `.env` file wasn't automatically loaded, causing the CrewAI agent to fail with missing API key errors. I fixed this by explicitly calling `load_dotenv()` at the start of the voice CLI script.

---

## Example Run and Insights

For my demo video, I tested the system with the following voice input:

**Voice Input:** *"Make the intro a bit more casual and mention my love for machine learning."*

**Whisper Transcription:** The `small` model transcribed my speech accurately: `"Make the intro a bit more casual and mention my love for machine learning."`

**Agent Processing:** The CrewAI system processed this request through its two-agent pipeline:
- The Profile Selector extracted key facts from my resume (name, program, background, interests)
- The Script Writer received both the profile outline and my voice request, then generated an introduction that incorporated the "casual tone" and "machine learning" emphasis

**Agent Output:**
```
Hi everyone, I'm Jessica! An avid lover of machine learning and data science 
pursuing my M.S. at Harvard. From Toronto to Cambridge, always ready for 
exciting challenges!
```

**TTS Synthesis:** Kokoro synthesized this text into natural-sounding speech, saved it to `response.wav`, and played it through my speakers.

### Key Insights

**Latency:** The total end-to-end latency was approximately 25-30 seconds: 8 seconds for recording (user-controlled), ~3 seconds for Whisper transcription, ~12-15 seconds for CrewAI agent execution (including LLM API calls and knowledge retrieval), and ~2 seconds for Kokoro TTS synthesis. The agent execution is the bottleneck—future optimizations could include streaming responses or using faster LLM models.

**Accuracy:** Whisper's transcription was excellent even with the `small` model. The agent successfully interpreted my voice request and adjusted both the tone (more casual) and content (emphasized machine learning). This demonstrates that the multi-agent system can effectively incorporate user preferences expressed through natural language.

**Voice Quality:** Kokoro produced high-quality, natural-sounding speech at 24kHz. The `af_bella` voice sounded clear and professional. The quality is comparable to commercial TTS services but runs entirely locally.

**User Experience:** Speaking to the agent felt more natural than typing, especially for quick requests like "make it more casual." However, the 25-30 second wait time between speaking and hearing the response felt long. For a production system, I would add visual/audio feedback during processing (e.g., "Transcribing...", "Thinking...", "Speaking...") to keep the user engaged.

**Design Trade-offs:** Running everything locally (Whisper + Kokoro) provides privacy and eliminates API costs, but requires more compute resources and setup (installing espeak-ng, downloading models). For users who prioritize convenience over privacy, cloud-based alternatives like OpenAI's Whisper API and TTS API would be simpler to deploy.

---

## Conclusion

Adding voice capabilities transformed my text-based agent into a conversational interface that feels more natural and accessible. The combination of local Whisper STT and Kokoro TTS creates a fully self-contained system that maintains user privacy while delivering high-quality voice interaction. The modular architecture makes it easy to swap components—for example, I could replace Kokoro with OpenAI's TTS API or add streaming capabilities for lower latency. This project demonstrated that building multimodal agents requires careful orchestration of multiple components (audio I/O, transcription, agent logic, synthesis) with attention to latency, accuracy, and user feedback at each stage.
