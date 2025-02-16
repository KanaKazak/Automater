import time
import pyautogui
import keyboard
import threading
import cv2
import numpy as np

# List of reference images
reference_images = ["C:\\Users\\1\\Desktop\\Automater\\sample1.png", "C:\\Users\\1\\Desktop\\Automater\\sample2.png", "C:\\Users\\1\\Desktop\\Automater\\sample3.png"]
stop_event = threading.Event()

def take_screenshot():
    return pyautogui.screenshot()

def analyze_screenshot(screenshot):
    screenshot_gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)
    for ref_img in reference_images:
        template = cv2.imread(ref_img, cv2.IMREAD_GRAYSCALE)
        if template is None:
            print(f"Error: Could not read {ref_img}")
            continue
        res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        if max_val > 0.8:
            h, w = template.shape
            center_x, center_y = max_loc[0] + w // 2, max_loc[1] + h // 2
            print(f"Match found with {ref_img} at ({center_x}, {center_y}), clicking...")
            pyautogui.click(center_x, center_y)
            return

def check_screenshots():
    while not stop_event.is_set():
        screenshot = take_screenshot()
        analyze_screenshot(screenshot)
        stop_event.wait(5)

def listen_for_quit():
    keyboard.wait('q')
    stop_event.set()
    print("Program stopped.")

if __name__ == "__main__":
    threading.Thread(target=check_screenshots).start()
    listen_for_quit()
