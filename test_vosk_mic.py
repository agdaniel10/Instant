import queue
import sounddevice as sd
from  vosk import Model, KaldiRecognizer
import json
import os
import sys

def main():
    # Configure your model path here
    # model_path = "models/vosk-model-small-en-us-0.15"
    model_path = "models/vosk-model-en-us-0.22-lgraph"
    
    # Verify model exists
    if not os.path.exists(model_path):
        print("=" * 60)
        print("❌ ERROR: Model not found!")
        print("=" * 60)
        print(f"Looking for model at: {os.path.abspath(model_path)}")
        print("\nPlease:")
        print("1. Extract the vosk zip file")
        print("2. Create a 'models' folder in your project")
        print("3. Move the extracted folder into 'models/'")
        print("\nExpected structure:")
        print("  your-project/")
        print("  ├── models/")
        print("  │   └── vosk-model-small-en-us-0.15/")
        print("  └── test_vosk_mic.py")
        print("=" * 60)
        sys.exit(1)
    
    print("=" * 60)
    print("VOSK MICROPHONE TEST")
    print("=" * 60)
    print(f"✅ Model found: {model_path}")
    print("⏳ Loading model... (this may take a few seconds)")
    
    try:
        model = Model(model_path)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        sys.exit(1)
    
    rec = KaldiRecognizer(model, 16000)
    q = queue.Queue()
    
    def audio_callback(indata, frames, time, status):
        if status:
            print(f"⚠️  Audio status: {status}", file=sys.stderr)
        q.put(bytes(indata))
    
    print("\n🎤 Using laptop microphone")
    print("📝 Speak clearly into your laptop")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 60)
    
    try:
        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype='int16',
            channels=1,
            callback=audio_callback
        ):
            while True:
                data = q.get()
                
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").strip()
                    if text:
                        print(f"\n✅ FINAL: {text}")
                else:
                    partial = json.loads(rec.PartialResult())
                    partial_text = partial.get("partial", "").strip()
                    if partial_text:
                        print(f"⏳ Partial: {partial_text}     ", end='\r')
    
    except KeyboardInterrupt:
        print("\n" + "-" * 60)
        print("🛑 Test stopped successfully")
        print("=" * 60)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()