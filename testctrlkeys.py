from pynput import keyboard

def on_press(key):
    try:
        if key == keyboard.Key.ctrl_l:
            print("Left Control key is pressed.")
        elif key == keyboard.Key.ctrl_r:
            print("Right Control key is pressed.")
    except AttributeError:
        pass

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener when Escape key is pressed
        return False

# Start listening for key events
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()




# # The keyboard module DOES NOT WORK BECAUSE THE KEYBOARD MODULE DOES NOT DISTINGUISH
# # BETWEEN THE TWO CONTROL KEYS

# import keyboard

# # Check if left control key is pressed
# if keyboard.is_pressed('ctrl'):
#     print("Left Control key is pressed.")

# # Check if right control key is pressed
# if keyboard.is_pressed('ctrl_r'):
#     print("Right Control key is pressed.")
    

