import pyautogui
import time
import keyboard
import threading

stop_event = threading.Event()

def check_stop():
    while not stop_event.is_set():
        if keyboard.is_pressed('q'):
            print("Auto-clicker stopping...")
            stop_event.set()

def auto_clicker(points=None):
    print("Auto-clicker starting in 5 seconds... Press 'q' to stop at any time.")
    
    stop_thread = threading.Thread(target=check_stop)
    stop_thread.start()

    for i in range(5, 0, -1):
        if stop_event.is_set():
            break
        print(i)
        time.sleep(1)

    if stop_event.is_set():
        print("Auto-clicker stopped.")
        return

    if not points:  # No points provided, click every second
        while not stop_event.is_set():
            pyautogui.click()
            print("Clicked at current mouse position")
            time.sleep(1)

    elif len(points) == 1:  # One point provided, click every second
        x, y = points[0]
        while not stop_event.is_set():
            pyautogui.click(x, y)
            print(f"Clicked at ({x}, {y})")
            time.sleep(1)

    else:  # Multiple points provided, click each with 3-second delay
        while not stop_event.is_set():
            for x, y in points:
                if stop_event.is_set():
                    break
                pyautogui.click(x, y)
                print(f"Clicked at ({x}, {y})")
                time.sleep(3)

    stop_event.set()
    stop_thread.join()
    print("Auto-clicker stopped.")

# Example usage:
# auto_clicker()  # No points, clicks every second
# auto_clicker([(500, 500)])  # One point, clicks every second
auto_clicker([(500, 500), (600, 600), (700, 700)])  # Multiple points, 3s delay
