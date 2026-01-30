from faster_whisper import WhisperModel

def load_model(model_size="small"):
    model = WhisperModel(
        model_size, 
        device="cpu", 
        compute_type="int8"
    )
    return model

def transcribe(model, audio_chunk, language="en"):
    # VAD parameters go here in transcribe(), not in model init
    segments, _ = model.transcribe(
        audio_chunk, 
        language=language,
        vad_filter=True,  # Move VAD here
        vad_parameters=dict(
            min_silence_duration_ms=500,
            threshold=0.5
        )
    )
    return segments