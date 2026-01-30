import pyaudio

def get_mic_stream(rate, chunk_size):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=rate,
        input=True,
        frames_per_buffer=chunk_size
    )
    return p, stream
