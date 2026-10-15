# Acoustic Echo Cancellation (AEC) & Hardware Loopback

The **Acoustic Echo Cancellation (AEC)** subsystem ([`src/jarvis/voice/audio_aec.py`](file:///C:/Users/deepa/OneDrive/Desktop/JARVIS-WORKSPACE/src/jarvis/voice/audio_aec.py)) enables true full-duplex voice interaction by eliminating speaker audio, system sounds, music, and background media from the microphone stream before it reaches cognitive models.

---

## 1. Problem Statement & Audio Isolation Challenge

When an AI assistant speaks through speakers, or when the operator plays music or videos on the host PC:
1. The sound travels across the physical room into the microphone.
2. Without AEC, the AI hears its own voice reflected into the microphone, triggering false interruptions, infinite audio feedback loops, and garbage transcription.
3. Conventional software filters only mute the microphone while speaking (half-duplex walkie-talkie mode), preventing the operator from interrupting naturally.

JARVIS resolves this by capturing the **exact digital speaker output** via Windows WASAPI loopback and mathematically subtracting it from the physical microphone stream.

---

## 2. DSP Engine Architecture

```mermaid
graph TD
    Speaker["🔊 Soundcard / Speakers"] -->|Physical Room Acoustic Path h(n)| Mic["🎤 Physical Microphone"]
    Speaker -->|WASAPI Loopback Capture x(n)| AEC["Partitioned Block Adaptive Filter W(f)"]
    Mic -->|Microphone Signal d(n) = s(n) + y(n)| Subtract["Subtract Filtered Echo: e(n) = d(n) - y_hat(n)"]
    AEC -->|Estimated Echo y_hat(n)| Subtract
    Subtract --> MSC["Magnitude Squared Coherence (MSC) Spectral Mask"]
    MSC --> CleanAudio["Clean Human Speech s(n)"] --> GeminiLive["⚡ Gemini 3.8 Live API"]
```

---

## 3. Mathematical Principles & Signal Processing

### 3.1 Partitioned Block Frequency Domain Adaptive Filter (PBFDAF)
Rather than computing costly time-domain convolutions across large impulse responses, JARVIS divides the acoustic filter into $P$ frequency-domain partitions (default: 6 partitions of block size $B = 256$ frames):

$$\hat{y}(m) = \sum_{p=0}^{P-1} \mathbf{W}_p(m) \mathbf{X}_p(m)$$

Where:
- $\mathbf{X}_p(m)$: Discrete Fourier Transform (DFT) of the $p$-th partition of the reference speaker audio $x(n)$.
- $\mathbf{W}_p(m)$: Adaptive complex filter weights representing the room's acoustic impulse response.
- $\hat{y}(m)$: Estimated echo signal arriving at the microphone.

### 3.2 Normalized Weight Update
Filter weights are updated dynamically using normalized least mean squares in the frequency domain:

$$\mathbf{W}_p(m+1) = \mathbf{W}_p(m) + \mu \frac{\mathbf{E}(m) \mathbf{X}_p^*(m)}{\sum_{p=0}^{P-1} \|\mathbf{X}_p(m)\|^2 + \epsilon}$$

Where $\mu$ is the adaptive step size (`AUDIO_AEC_STEP_SIZE = 0.25`) and $\mathbf{E}(m)$ is the error spectrum:

$$\mathbf{E}(m) = \mathbf{D}(m) - \hat{\mathbf{Y}}(m)$$

### 3.3 Magnitude Squared Coherence (MSC) Post-Filter
To eliminate nonlinear residual echoes caused by physical speaker enclosure vibrations, JARVIS applies a post-adaptive spectral suppression mask:

$$\gamma_{dx}^2(f) = \frac{|S_{dx}(f)|^2}{S_{dd}(f) S_{xx}(f)}$$

When coherence $\gamma_{dx}^2(f)$ is close to $1.0$, the frequency bin contains pure speaker echo and is suppressed by up to $30\text{ dB}$ (`AUDIO_AEC_SUPPRESSION_DB`). When coherence drops, human voice is detected and passed through unattenuated.

---

## 4. Windows WASAPI Loopback Capture Implementation

The loopback capture worker runs in a dedicated high-priority background thread:

```python
# COM WASAPI Endpoint Initialization
enumerator = AudioUtilities.GetDeviceEnumerator()
default_render = enumerator.GetDefaultAudioEndpoint(eRender, eMultimedia)
audio_client = default_render.Activate(IID_IAudioClient, CLSCTX_ALL, None)
# Initialize in AUDCLNT_STREAMFLAGS_LOOPBACK mode
audio_client.Initialize(
    AUDCLNT_SHAREMODE_SHARED,
    0x00020000,  # AUDCLNT_STREAMFLAGS_LOOPBACK
    buffer_duration,
    0,
    mix_format,
    None,
)
```

- **Resampling:** Automatically downsamples system audio (typically 48kHz or 44.1kHz stereo) to the reference rate of 16kHz mono using high-quality polyphase filtering.
- **Silent Frame Protection:** Handles `AUDCLNT_BUFFERFLAGS_SILENT` gracefully by emitting true zero buffers without CPU spikes.

---

## 5. Diagnostic Health Metrics

The AEC subsystem exports runtime telemetry via `audio_aec.get_diagnostics()`:

| Metric | Normal Range | Meaning |
| :--- | :--- | :--- |
| **Echo Return Loss Enhancement (ERLE)** | $18\text{ dB} - 35\text{ dB}$ | Ratio of uncancelled speaker energy to cancelled residual energy. Higher is better. |
| **Loopback Packet Capture Rate** | $95\% - 100\%$ | Integrity of the WASAPI capture thread. |
| **Double-Talk Flag** | `True` / `False` | Detects when operator and assistant speak simultaneously. |
| **Adaptive Filter Norm** | Stable non-zero | Verifies filter convergence against room acoustics. |
