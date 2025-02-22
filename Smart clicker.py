import time
import pytesseract
import pyautogui
import cv2
import numpy as np
import keyboard
import threading

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

screenshot_interval = 3  # Interval in seconds to take screenshots
# List of reference images
reference_images = ["D:\\Automater-main\\Automater-main\\sample1.png", "D:\\Automater-main\\Automater-main\\sample2.png", "D:\\Automater-main\\Automater-main\\sample3.png"]

# List of triggers (text to detect on buttons)
triggers = ["Download", "SLOW DOWNLOAD", "Continue"]

stop_event = threading.Event()

def take_screenshot():
    return pyautogui.screenshot()

def analyze_screenshot(screenshot):
    screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    screenshot_gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
    
    for ref_img in reference_images:
        template = cv2.imread(ref_img, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print(f"Error: Could not read {ref_img}")
            continue
        
        h, w = template.shape
        res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Adjust this threshold as needed
        loc = np.where(res >= threshold)
        
        for pt in zip(*loc[::-1]):
            x, y = pt[0] + w // 2, pt[1] + h // 2
            roi = screenshot_cv[y - h//2:y + h//2, x - w//2:x + w//2]  # Extract ROI
            roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            
            detected_text = pytesseract.image_to_string(roi_gray).strip().lower()
            print(f"Detected text: {detected_text}")
            
            for trigger in triggers:
                if trigger in detected_text:
                    print(f"Match found: '{trigger}' at ({x}, {y}), clicking...")
                    pyautogui.click(x, y)
                    return

def check_screenshots():
    while not stop_event.is_set():
        screenshot = take_screenshot()
        analyze_screenshot(screenshot)
        stop_event.wait(screenshot_interval)

def listen_for_quit():
    keyboard.wait('q')
    stop_event.set()
    print("Program stopped.")

if __name__ == "__main__":
    threading.Thread(target=check_screenshots).start()
    listen_for_quit()
