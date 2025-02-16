import time
import pytesseract
import pyautogui
from PIL import Image
import keyboard
import threading

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

click_position = (500, 500)
target_text = "are you sure you want to download the file?"

stop_event = threading.Event()

def take_screenshot():
    return pyautogui.screenshot()

def analyze_screenshot(screenshot):
    return pytesseract.image_to_string(screenshot)

def check_screenshots():
    while not stop_event.is_set():
        screenshot = take_screenshot()
        extracted_text = analyze_screenshot(screenshot)
        print("Extracted Text:", extracted_text)

        if target_text.lower() in extracted_text.lower():
            print("Target text found! Clicking at", click_position)
            pyautogui.click(click_position)

        stop_event.wait(5)

def listen_for_quit():
    keyboard.wait('q')
    stop_event.set()
    print("Program stopped.")

if __name__ == "__main__":
    threading.Thread(target=check_screenshots).start()
    listen_for_quit()