# Smart Clicker Script
# This script automates mouse clicks based on text recognition from the screen.
# Required Libraries:
# - easyocr: For Optical Character Recognition (OCR)
# - pyautogui: For mouse control
# - cv2: For image processing
# - keyboard: For keyboard event handling
# - time: For sleep functionality
# - numpy: For numerical operations
# - threading: For running the monitoring in a separate thread
import time
import pyautogui
import cv2
import numpy as np
import threading
import keyboard
import easyocr

# Reference images of the buttons to look for
reference_images = ["sample1.png", "sample2.png", "sample3.png"]
# Texts we want to trigger on
triggers = ["SLOW DOWNLOAD", "Download", "Continue"]

# Create OCR reader (English only to keep it fast)
reader = easyocr.Reader(['en'], gpu=False)

# Stop flag
stop_event = threading.Event()

def take_screenshot():
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def find_buttons_and_click(frame):
    for ref_path in reference_images:
        template = cv2.imread(ref_path)
        if template is None:
            print(f"[ERROR] Couldn't read reference image: {ref_path}")
            continue

        h, w = template.shape[:2]
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        locations = np.where(result >= threshold)

        for pt in zip(*locations[::-1]):
            x, y = pt
            roi = frame[y:y+h, x:x+w]

            # Run OCR on the cropped button
            result = reader.readtext(roi, detail=0)
            print(f"[DEBUG] OCR Result: {result}")

            for text in result:
                for trigger in triggers:
                    if trigger.lower() in text.lower():
                        print(f"[MATCH] Found '{trigger}' in button at ({x + w//2}, {y + h//2}), clicking...")
                        pyautogui.click(x + w//2, y + h//2)
                        return  # Stop after first match

def monitor_screen():
    print("[INFO] Started screen monitoring. Press 'q' to quit.")
    while not stop_event.is_set():
        screenshot = take_screenshot()
        find_buttons_and_click(screenshot)
        stop_event.wait(5)

def listen_for_quit():
    keyboard.wait("q")
    stop_event.set()
    print("[INFO] Quit signal received. Stopping...")

if __name__ == "__main__":
    threading.Thread(target=monitor_screen).start()
    listen_for_quit()
    print("[INFO] Main thread is running. Press 'q' to stop the script.")
    stop_event.set()
    print("[INFO] Script has stopped.")
# End of Smart Clicker Script
# Note: Ensure you have the required libraries installed:
# pip install easyocr pyautogui opencv-python keyboard numpy
# Make sure to run this script with appropriate permissions to control the mouse.
# Also, ensure the reference images are in the same directory as this script or provide the correct paths.
# This script is designed to run indefinitely until the user presses 'q'.