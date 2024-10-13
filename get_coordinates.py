import pyautogui
import time

# Continuously print mouse position
while True:
    x, y = pyautogui.position()  # Get current mouse coordinates
    print(f"Mouse position: ({x}, {y})")
    time.sleep(1)  # Update every 1 second
