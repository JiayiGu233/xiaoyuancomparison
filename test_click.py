import pyautogui
import time
import keyboard

def click_buttons():
    pyautogui.click(1608, 451)  # Click "Accept Happily" button
    time.sleep(0.3)
    pyautogui.click(1751, 985)  # Click "Continue" button
    time.sleep(0.3)
    pyautogui.click(1664, 833)  # Click "Continue PK" button

def main():
    print("Press 'Space' to trigger the click sequence, or 'Esc' to exit.")

    # Keep running the loop to detect key presses
    while True:
        if keyboard.is_pressed('space'):
            click_buttons()
            time.sleep(0.5)  # Add a small delay to prevent multiple triggers
        elif keyboard.is_pressed('esc'):
            print("Exiting program...")
            break
 
if __name__ == "__main__":
    main()
