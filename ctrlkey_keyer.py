'''
Working iambic keyer, using Ctrl_l and Ctrl_r on keyboard, which is what vband sends

created with much help from ChatGPT.  Which can be enormously dunderheaded but works if
you are very clear in your specification
prompt:
an iambic keyer script for linux using Ctrl_L for dah and Ctrl_R for dit.  
When both keys are pressed the output should iterate between a dit followed by a space equal to 3 dits followed by a dah followed by a space equal to 6 dits. 
If only one key is pressed, then do the following: Holding down Ctrl_R should produce a sequence of dits. Holding down Ctrl_L should produce a sequence of dahs.  In all cases: every dit should always be followed by a space equal in duration to 3 dits and every dah should be followed by a space equal in duration to 6 dits.  
Sound should be mono and alsa should be used.   Dits and dahs should have the same pitch, but dahs should have 3 times the duration of dits.   Dits and dahs and spaces should never overlap.

TODO: take wpm as an argument and calculate durations from that
TODO: update logic to enable true iambic behavior, and take an option for A or B
TODO: take sidetone pitch as an argument, with a reasonable default
'''

import time
import pygame
import numpy as np
from pynput import keyboard

# Constants for timing (in seconds)
#
DOT_TIME = 0.05  # Duration of a dit (1 unit of time)
DASH_TIME = DOT_TIME * 3.15  # Duration of a dah (3.15 units of time)
SPACE_BETWEEN_DITS = DOT_TIME * 3  # Space after a dit (3 dot times)
SPACE_BETWEEN_DAHS = DOT_TIME * 6  # Space after a dah (6 dot times)
SPACE_BETWEEN_TONES = 0  # between alternating pairs of dahs and dits when squeezed

# Audio settings
SAMPLE_RATE = 44100  # Audio sample rate (samples per second)
MORSE_FREQ = 600  # Frequency for both dits and dahs (Hz)
pygame.mixer.init(frequency=SAMPLE_RATE, channels=1)  # Mono output

# Global state variables
dot_pressed = False
dash_pressed = False
last_time = time.time()  # Track time for proper pacing
last_key_pressed = None  # Track the last key pressed to alternate tones

# Function to generate a sine wave tone
def generate_tone(frequency, duration):
    """Generate a sine wave tone and play it."""
    samples = int(SAMPLE_RATE * duration)
    t = np.linspace(0, duration, samples, endpoint=False)  # Time values
    tone = np.sin(2 * np.pi * frequency * t)  # Mono tone (1 channel)

    # Normalize to the range [-32767, 32767] (16-bit signed PCM)
    tone = np.int16(tone * 32767)

    # Create sound object and play it
    sound = pygame.sndarray.make_sound(tone)
    sound.play()

# Handle key press events
def on_press(key):
    global dot_pressed, dash_pressed

    try:
        if key == keyboard.Key.ctrl_r:
            dot_pressed = True  # Ctrl_R pressed for dit
        elif key == keyboard.Key.ctrl_l:
            dash_pressed = True  # Ctrl_L pressed for dah
        elif key == keyboard.Key.esc:
            print("Esc key pressed, exiting...")
            return False  # Stop the listener and exit
    except AttributeError:
        pass  # Handle non-ASCII keys gracefully

# Handle key release events
def on_release(key):
    global dot_pressed, dash_pressed

    try:
        if key == keyboard.Key.ctrl_r:
            dot_pressed = False  # Ctrl_R released
        elif key == keyboard.Key.ctrl_l:
            dash_pressed = False  # Ctrl_L released
    except AttributeError:
        pass

# Main function for the iambic keyer
def iambic_keyer():
    global last_time, last_key_pressed

    print("Iambic Keyer")
    print("Press Ctrl_L for dahs, Ctrl_R for dits.")
    print("Press both together for alternating dits and dahs.")
    print("Press Esc to quit.")

    # Start listener for key press/release
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        while True:
            current_time = time.time()

            # When only Ctrl_R is pressed (dit only)
            if dot_pressed and not dash_pressed:
                if current_time - last_time >= DOT_TIME:
                    generate_tone(MORSE_FREQ, DOT_TIME)  # Play dit
                    last_time = current_time
                    last_key_pressed = 'dot'
                    time.sleep(SPACE_BETWEEN_DITS)  # Space after the dit

            # When only Ctrl_L is pressed (dah only)
            elif dash_pressed and not dot_pressed:
                if current_time - last_time >= DOT_TIME:
                    generate_tone(MORSE_FREQ, DASH_TIME)  # Play dah
                    last_time = current_time
                    last_key_pressed = 'dash'
                    time.sleep(SPACE_BETWEEN_DAHS)  # Space after the dah

            # When both Ctrl_R and Ctrl_L are pressed (alternating dits and dahs)
            elif dot_pressed and dash_pressed:
                if current_time - last_time >= DOT_TIME:
                    if last_key_pressed != 'dash':  # If last was not a dah, play dah
                        generate_tone(MORSE_FREQ, DASH_TIME)  # Play dah
                        last_key_pressed = 'dash'
                        time.sleep(SPACE_BETWEEN_DAHS)  # Space after dah
                    else:  # If last was a dah, play dit
                        generate_tone(MORSE_FREQ, DOT_TIME)  # Play dit
                        last_key_pressed = 'dot'
                        time.sleep(SPACE_BETWEEN_DITS)  # Space after dit

                    last_time = current_time
                    time.sleep(SPACE_BETWEEN_TONES)  # Small space between alternating tones

            # Small delay to avoid high CPU usage
            time.sleep(0.01)

# Start the keyer
if __name__ == "__main__":
    iambic_keyer()
