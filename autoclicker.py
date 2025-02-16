import pyautogui
import threading
import time

def auto_clicker(interval=1.0, key=None, button='left'):
    try:
        while not stop_event.is_set():
            if key:
                pyautogui.press(key)
            else:
                pyautogui.click(button=button)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Auto-clicker stopped.")

def listen_for_quit():
    input("Press 'q' and Enter to stop...\n")
    stop_event.set()

stop_event = threading.Event()

interval = float(input("Enter the interval in seconds between clicks/keypresses: "))
key = input("Enter a key to press (leave empty for mouse clicks): ")
button = 'left'
if not key:
    button = input("Enter mouse button to click (left, right, middle): ") or 'left'

click_thread = threading.Thread(target=auto_clicker, args=(interval, key, button))
quit_thread = threading.Thread(target=listen_for_quit)

click_thread.start()
quit_thread.start()

click_thread.join()
quit_thread.join()

print("Auto-clicker terminated.")
