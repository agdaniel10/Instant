from faster_whisper import WhisperModel
import pyaudio
import numpy as np
import threading
import queue
import os

class UltraFastTranscriber:
    def __init__(self):
        # Use the absolute fastest settings
        self.model = WhisperModel(
            "small.en",
            device="cpu",
            compute_type="int8",
            cpu_threads=os.cpu_count(),  # Automatically use all cores
            num_workers=1
        )
        
        self.audio_queue = queue.Queue(maxsize=10)
        self.result_queue = queue.Queue()
        
    def audio_worker(self):
        """Capture audio in background"""
        RATE = 16000
        CHUNK = 1024
        
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )
        
        buffer = []
        frames_per_chunk = int(RATE / CHUNK * 2)  # 2-second chunks
        
        while True:
            data = stream.read(CHUNK, exception_on_overflow=False)
            buffer.append(np.frombuffer(data, dtype=np.int16))
            
            if len(buffer) >= frames_per_chunk:
                audio = np.concatenate(buffer).astype(np.float32) / 32768.0
                self.audio_queue.put(audio)
                buffer = buffer[-int(frames_per_chunk * 0.2):]  # 20% overlap
    
    def transcription_worker(self):
        """Process audio in background"""
        while True:
            audio = self.audio_queue.get()
            
            # Ultra-fast settings
            segments, _ = self.model.transcribe(
                audio,
                beam_size=1,  # Greedy decoding (fastest)
                best_of=1,
                language="en",
                condition_on_previous_text=False,  # Faster
                vad_filter=True,
                vad_parameters=dict(
                    threshold=0.5,
                    min_speech_duration_ms=250
                )
            )
            
            for segment in segments:
                self.result_queue.put(segment.text)
    
    def start(self):
        # Start both workers
        threading.Thread(target=self.audio_worker, daemon=True).start()
        threading.Thread(target=self.transcription_worker, daemon=True).start()
        
        print("🎤 Ultra-fast transcription started...")
        
        while True:
            try:
                text = self.result_queue.get(timeout=0.1)
                print(f"📝 {text}")
            except queue.Empty:
                continue

# Usage
transcriber = UltraFastTranscriber()
transcriber.start()