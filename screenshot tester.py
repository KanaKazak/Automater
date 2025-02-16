import time
import pytesseract
import pyautogui
from PIL import Image
import keyboard

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Coordinates to click if text is found (change as needed)
click_position = (500, 500)  # Example coordinates

# Target text to search for in the screenshot
target_text = "are you sure you want to download the file?"

def take_screenshot():
    screenshot = pyautogui.screenshot()
    return screenshot

def analyze_screenshot(screenshot):
    text = pytesseract.image_to_string(screenshot)
    return text

def main():
    print("Running screenshot checker... Press 'q' to quit.")
    while True:
        if keyboard.is_pressed('q'):
            print("Program stopped.")
            break
        
        screenshot = take_screenshot()
        extracted_text = analyze_screenshot(screenshot)
        print("Extracted Text:", extracted_text)

        if target_text.lower() in extracted_text.lower():
            print("Target text found! Clicking at", click_position)
            pyautogui.click(click_position)
        
        time.sleep(5)  # Wait for 5 seconds before taking another screenshot

if __name__ == "__main__":
    main()
