import time
import pyautogui
import keyboard
import threading
import cv2
import numpy as np
import easyocr
import glob  # For finding multiple reference images

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])

screenshot_interval = 3 # Interval in seconds to take screenshots


# Load all reference images dynamically
template_files = glob.glob("sample*.png")  # Finds all files like "sample1.png", "sample2.png", etc.
templates = [cv2.imread(file, cv2.IMREAD_GRAYSCALE) for file in template_files]

# List of triggers to search for in the button text
triggers = ["Download", "SLOW DOWNLOAD", "Continue"]

stop_event = threading.Event()

def take_screenshot():
    return pyautogui.screenshot()

def find_buttons(screenshot):
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    found_buttons = []

    for template in templates:
        if template is None:
            continue

        h, w = template.shape

        # Template matching
        res = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Adjust as needed
        loc = np.where(res >= threshold)

        for pt in zip(*loc[::-1]):
            x, y = pt[0] + w // 2, pt[1] + h // 2  # Click center of detected button
            button_region = screenshot_cv[y:y+h, pt[0]:pt[0]+w]  # Crop button region
            found_buttons.append((x, y, button_region))
    
    return found_buttons  # Returns a list of button positions and cropped images

def check_text(button_region):
    if button_region is None or button_region.size == 0:
        return False

    results = reader.readtext(button_region)
    for _, text, _ in results:
        if any(trigger.lower() in text.lower() for trigger in triggers):
            print(f"Found matching text: '{text}'")
            return True
    
    return False

def find_and_click():
    while not stop_event.is_set():
        screenshot = take_screenshot()
        buttons = find_buttons(screenshot)

        for x, y, button_region in buttons:
            if check_text(button_region):  # Click only if text matches
                print(f"Clicking button at ({x}, {y})")
                pyautogui.click(x, y)

        stop_event.wait(screenshot_interval)

def listen_for_quit():
    keyboard.wait('q')
    stop_event.set()
    print("Program stopped.")

if __name__ == "__main__":
    threading.Thread(target=find_and_click).start()
    listen_for_quit()
