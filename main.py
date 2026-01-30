import time
import numpy as np
import threading
from config import MIC_RATE, CHUNK_SIZE, MODEL_SIZE, LANGUAGE
from audio.mic_stream import get_mic_stream
from transcription.whisper_model import load_model, transcribe
from detection.regex_detector import detect_verses
from bible.lookup import get_verse
from display.gui_display import VerseDisplay

# Setup
p, stream = get_mic_stream(MIC_RATE, CHUNK_SIZE)
model = load_model(MODEL_SIZE)
display = VerseDisplay()

# Sliding text buffer
buffer_text = ""

# Common hallucination phrases to filter out
HALLUCINATION_PHRASES = [
    "thank you",
    "thanks for watching",
    "see you in the next video",
    "subscribe",
    "like and subscribe",
    "don't forget to",
    "please like",
    "hit the bell",
]

def is_hallucination(text):
    """Check if text is likely a hallucination"""
    text_lower = text.lower().strip()
    
    # Ignore very short or empty transcriptions
    if len(text_lower) < 3:
        return True
    
    # Ignore if it's just punctuation or single words like "you", "done", "good"
    single_word_noise = ["you", "done", "good", "okay", "um", "uh", "ah"]
    if text_lower in single_word_noise:
        return True
    
    # Check against known hallucinations
    for phrase in HALLUCINATION_PHRASES:
        if phrase in text_lower:
            return True
    
    return False

def audio_processing_loop():
    """Runs in background thread - listens and processes audio"""
    global buffer_text
    
    try:
        print("Listening... Ctrl+C to stop")
        while True:
            # Read audio chunk
            data = stream.read(CHUNK_SIZE*20, exception_on_overflow=False)
            audio_np = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            
            # Transcribe
            segments = transcribe(model, audio_np, LANGUAGE)
            for segment in segments:
                # Filter out hallucinations
                if is_hallucination(segment.text):
                    print(f"[Filtered hallucination]: {segment.text}")
                    continue
                
                buffer_text += " " + segment.text
                print(f"Transcribed: {segment.text}")  # Debug output
            
            # Detect verses
            detected = detect_verses(buffer_text)
            for book, chapter, vs, ve in detected:
                verse_text = get_verse(book, chapter, vs, ve)
                display_text = f"{book} {chapter}:{vs}-{ve}\n\n{verse_text}"
                print(f"Detected: {book} {chapter}:{vs}-{ve}")  # Debug output
                display.update_verse(display_text)
                
                # Clear buffer for next detection
                buffer_text = ""
                # After building buffer_text
                if buffer_text.strip():
                    print(f"Buffer content: '{buffer_text}'")  # Add this
                    detected = detect_verses(buffer_text)
                
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

# Start audio processing in background thread
audio_thread = threading.Thread(target=audio_processing_loop, daemon=True)
audio_thread.start()

# Start GUI (this blocks, but audio runs in background)
print("Starting GUI...")
display.start()