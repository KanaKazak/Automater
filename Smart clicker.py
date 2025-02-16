import time
import pytesseract
import pyautogui
from PIL import Image
import keyboard
import threading
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# List of triggers to search for in the screenshot
triggers = ["yes", "confirm", "ok"]

stop_event = threading.Event()

def take_screenshot():
    return pyautogui.screenshot()

def analyze_screenshot(screenshot):
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    data = pytesseract.image_to_data(screenshot_cv, output_type=pytesseract.Output.DICT)
    return data

def find_and_click_text(data):
    for trigger in triggers:
        for i, text in enumerate(data['text']):
            if trigger.lower() in text.lower():
                x = data['left'][i] + data['width'][i] // 2
                y = data['top'][i] + data['height'][i] // 2
                print(f"Found '{trigger}' at ({x}, {y}), clicking...")
                pyautogui.click(x, y)
                return

def check_screenshots():
    while not stop_event.is_set():
        screenshot = take_screenshot()
        data = analyze_screenshot(screenshot)
        find_and_click_text(data)
        stop_event.wait(5)

def listen_for_quit():
    keyboard.wait('q')
    stop_event.set()
    print("Program stopped.")

if __name__ == "__main__":
    threading.Thread(target=check_screenshots).start()
    listen_for_quit()