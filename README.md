ctrlkey_keyer.py

Works with vband dongle (or clone) so you can practice sending with paddles on your computer.
You can also just use a couple of keys on your keyboard as paddles.

Plug the dongle into a USB port on your computer, then plug your paddles into the dongle.

Python script provides an iambic morse code keyer 
where Ctrl_R and Ctrl_L produce dits and dahs with appropriate spacing, 
and alternating when both keys are pressed simultaneously. The sound is generated using pygame and played via ALSA on Linux in mono output.

The Vband dongle generates Ctrl_R and Ctrl_L keypress events, 
so this will work with it locally

Dependencies: pygame pynput numpy

Explanation of the Code:

    Timing Constants:
        DOT_TIME represents the duration of a dit.
        DASH_TIME is 3 times the duration of a dit and represents the duration of a dah.
        The spaces between dits and dahs are set to 3 and 6 dits, respectively.
        (TODO: refine this, make wpm an option)

    Audio Generation:
        The generate_tone function generates a sine wave at a frequency of 600 Hz for both dits and dahs. It uses numpy to generate the audio samples and pygame to play them.

    Key Press Handling:
        The on_press and on_release functions use the pynput library to detect when Ctrl_L (dah) and Ctrl_R (dit) are pressed or released.
        When Ctrl_L is pressed, it sets dash_pressed = True, and when Ctrl_R is pressed, it sets dot_pressed = True.

    Key Behavior:
        If only Ctrl_R is pressed, it generates a continuous sequence of dits, each followed by a space of 3 dits.
        If only Ctrl_L is pressed, it generates a continuous sequence of dahs, each followed by a space of 6 dits.
        If both Ctrl_R and Ctrl_L are pressed simultaneously, the script alternates between dits and dahs, maintaining their respective timings and spaces.
        (TODO: refine this to reflect true iambic behavior, and make A/B an option)
    Timing Control:
        The time.sleep function ensures that the spaces between dits, dahs, and alternating tones are respected and that there is no overlap between dits, dahs, or spaces.

    Ending the Program:
        Pressing the Esc key will stop the listener and exit the loop.

To Run:
    sudo python3 ./ctlkey_keyer.py




