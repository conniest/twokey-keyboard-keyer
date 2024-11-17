import numpy as np
import sounddevice as sd
from pynput import keyboard

# Parameters for the tone
SAMPLE_RATE = 44100  # Samples per second
FREQUENCY = 440  # Frequency of the tone (Hz), A4 note (440 Hz)
DURATION = 0.5  # Duration of the tone (seconds)

def generate_tone(frequency, duration, sample_rate):
    # Generate a tone using numpy (sine wave)
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    tone = 0.5 * np.sin(2 * np.pi * frequency * t)
    return tone

def on_press(key):
    try:
        # If the right Ctrl key is pressed
        if key == keyboard.Key.ctrl_r:
            print("Right Ctrl pressed, playing tone!")
            # Generate and play the tone
            tone = generate_tone(FREQUENCY, DURATION, SAMPLE_RATE)
            sd.play(tone, SAMPLE_RATE)
            sd.wait()  # Wait until the sound has finished playing
    except AttributeError:
        pass

def on_release(key):
    # Stop listener when the Escape key is pressed
    if key == keyboard.Key.esc:
        return False

# Set up listener for keyboard events
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
