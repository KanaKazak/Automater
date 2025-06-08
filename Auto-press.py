import pyautogui
pyautogui.FAILSAFE = False
import threading
import time
import keyboard  # Added library for listening to keypresses


def auto_clicker(interval=1.0, key=None, button='left', hold=False):
    try:
        while not stop_event.is_set():
            if key:
                if hold:
                    pyautogui.keyDown(key)
                    time.sleep(interval)
                    pyautogui.keyUp(key)
                else:
                    pyautogui.press(key)
            else:
                if hold:
                    pyautogui.mouseDown(button=button)
                    time.sleep(interval)
                    pyautogui.mouseUp(button=button)
                else:
                    pyautogui.click(button=button)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Auto-clicker stopped.")

# Set parameters directly in code
interval = 0.5
key = None  # Example: 'a'
button = 'left'  # Options: 'left', 'right', 'middle'
hold = False  # Set to True to press and hold

stop_event = threading.Event()

click_thread = threading.Thread(target=auto_clicker, args=(interval, key, button, hold))
click_thread.start()

print("Press 's' to stop the auto-clicker.")
keyboard.wait('s')  # Wait for 's' key press
stop_event.set()

click_thread.join()
print("Auto-clicker terminated.")