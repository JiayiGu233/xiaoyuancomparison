# -*- coding: latin-1 -*-

print("Script is running")
import cv2
import numpy as np
import pyautogui
import pytesseract
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time
import pygetwindow as gw
import re
import sys
import keyboard
import os
import glob


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Set the path for Tesseract-OCR



# Variables to track state
not_found_count = 0
last_not_found_time = 0
last_numbers = None  # Store the last recognized numbers
skip_count = 0  # Skip count tracker

def window_xy():
    windows = gw.getWindowsWithTitle('BlueStacks App Player')  # Ensure window title contains 'BlueStacks'
    if not windows:
        raise Exception("BlueStacks window not found, make sure BlueStacks is running.")
    bluestacks_window = windows[0]

    # Ensure the window is active
    if not bluestacks_window.isActive:
        bluestacks_window.activate()
        time.sleep(0.5)  # Wait for window activation

    # Get window position
    window_x, window_y = bluestacks_window.topleft
    # window_width, window_height = bluestacks_window.size
    return window_x, window_y

SCREENSHOT_DIR = "screenshots"

def capture_area():
    
    # Screenshot region relative to window (x, y, width, height)
    region_relative_left = (200, 328, 140, 54)
    region_relative_right = (402, 326, 140, 54)

    x, y = window_xy()
    # Calculate absolute screen coordinates
    region_absolute_left = (
        x + region_relative_left[0],
        y + region_relative_left[1],
        region_relative_left[2],
        region_relative_left[3]
    )
    region_absolute_right = (
        x + region_relative_right[0],
        y + region_relative_right[1],
        region_relative_right[2],
        region_relative_right[3]
    )

    # Take a screenshot
    screenshot_left = pyautogui.screenshot(region=region_absolute_left)
    screenshot_right = pyautogui.screenshot(region=region_absolute_right)

    left_image = np.array(screenshot_left)
    right_image = np.array(screenshot_right)

    left_image_path = os.path.join(SCREENSHOT_DIR, "left.png")
    right_image_path = os.path.join(SCREENSHOT_DIR, "right.png")
    
    # 将图像从RGB转换为BGR，以便与OpenCV兼容
    left_bgr = cv2.cvtColor(left_image, cv2.COLOR_RGB2BGR)
    right_bgr = cv2.cvtColor(right_image, cv2.COLOR_RGB2BGR)

    # 保存图像
    cv2.imwrite(left_image_path, left_bgr)
    cv2.imwrite(right_image_path, right_bgr)

    # Return both images as a tuple
    return left_image, right_image



# def recognize_numbers(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
#     text = pytesseract.image_to_string(thresh, config='--psm 6')
#     print(f"Raw recognized text: {text}")

#     numbers = [int(s) for s in text.split() if s.isdigit()]
#     print(f"numbers extracted: {numbers}")  # 打印识别的所有数字列表
#     return numbers

# def recognize_single_image(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)[1]
#     custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'
#     return pytesseract.image_to_string(thresh, config=custom_config)

# def recognize_numbers_parallel(left_image, right_image):
#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         future_left = executor.submit(recognize_single_image, left_image)
#         future_right = executor.submit(recognize_single_image, right_image)
        
#         text_left = future_left.result()
#         text_right = future_right.result()

#         text_left = re.sub(r'[^0-9]', '', text_left)
#         text_right = re.sub(r'[^0-9]', '', text_right)

#         numbers_left = [int(s) for s in re.findall(r'\d+', text_left)]
#         numbers_right = [int(s) for s in re.findall(r'\d+', text_right)]
        
#     numbers = numbers_left + numbers_right
#     # print(f"numbers extracted: {numbers}")
#     return numbers

def recognize_numbers(left_image, right_image):
    # Convert both images to grayscale
    gray_left = cv2.cvtColor(left_image, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(right_image, cv2.COLOR_BGR2GRAY)
    # gray_left = cv2.resize(gray_left, (0, 0), fx=0.5, fy=0.5)
    # gray_right = cv2.resize(gray_right, (0, 0), fx=0.5, fy=0.5)

    # Apply thresholding to both images (use only the second value from cv2.threshold)
    _, thresh_left = cv2.threshold(gray_left, 128, 255, cv2.THRESH_BINARY)
    _, thresh_right = cv2.threshold(gray_right, 128, 255, cv2.THRESH_BINARY)

    # custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789'

    # Recognize numbers in both the left and right images
    text_left = pytesseract.image_to_string(thresh_left, config='--psm 6')
    text_right = pytesseract.image_to_string(thresh_right, config='--psm 6')

    text_left = text_left.replace('A', '4')
    text_right = text_right.replace('A', '4')
    # text_left = re.sub(r'[^0-9]', '', text_left)
    # text_right = re.sub(r'[^0-9]', '', text_right)

    print(f"Raw recognized text (left): {text_left}", end='')
    print(f"Raw recognized text (right): {text_right}", end='')

    # Extract digits from the recognized text
    numbers_left = [int(s) for s in re.findall(r'\d+', text_left)]
    numbers_right = [int(s) for s in re.findall(r'\d+', text_right)]

    # Combine the numbers from both sides
    numbers = numbers_left + numbers_right
    print(f"numbers extracted: {numbers}")
    return numbers

def handle_insufficient_numbers():
    global not_found_count, last_not_found_time

    current_time = time.time()
    not_found_count = not_found_count + 1 if current_time - last_not_found_time <= 1 else 1
    last_not_found_time = current_time

    print("Not enough numbers found for comparison")
    if not_found_count >= 25:
        click_buttons()
        time.sleep(10)
        print("Preparing to restart the program...")
        time.sleep(0.3)
        main()

def click_buttons():
    x, y = window_xy()
    pyautogui.click(x+372, y+602)  # Click "Accept Happily" button
    time.sleep(0.3)
    pyautogui.click(x+542, y+1303)  # Click "Continue" button
    time.sleep(0.5)
    pyautogui.click(x+410, y+1141)  # Click "Continue PK" button
    time.sleep(0.3)

def draw_comparison(numbers):
    global not_found_count, last_numbers, skip_count

    if len(numbers) < 2:
        handle_insufficient_numbers()
        return

    # If the current numbers are the same as the last numbers, increase the skip count
    if last_numbers is not None and last_numbers == numbers:
        skip_count += 1
        print(f"Current result is the same as last time, skipping this execution (count: {skip_count})")
        if skip_count > 5:  # If skip count exceeds 5, force execution
            skip_count = 0
            execute_drawing_logic(numbers)
        return

    execute_drawing_logic(numbers)  # Execute the drawing logic with current numbers

    not_found_count = 0  # Reset not found count
    last_numbers = numbers  # Update last recognized numbers
    skip_count = 0  # Reset skip count

def execute_drawing_logic(numbers):
    first, second = numbers[:2]  # Get the first two numbers
    # print(f"execute_drawing_logic with Recognized numbers: {first}, {second}")

    if first > second:
        print(f"{first} > {second}")
        draw_greater_than()
        
    elif first < second:
        print(f"{first} < {second}")
        draw_less_than()

def draw_greater_than():

    x,y=window_xy()
    start_x, start_y = x+320, y+776

    # 模拟鼠标按下并绘制大于号
    pyautogui.moveTo(start_x, start_y)  # 移动到起始位置
    pyautogui.mouseDown()  # 按下鼠标
    pyautogui.moveTo(start_x + 50, start_y + 50, duration=0.001)  # 向上移动绘制第一条线
    pyautogui.moveTo(start_x, start_y + 100, duration=0.001)  # 向下移动绘制第二条线
    pyautogui.mouseUp()  # 松开鼠标

# 手写“小于”符号
def draw_less_than():

    x,y=window_xy()

    start_x, start_y = x+320, y+776

    # 模拟鼠标按下并绘制小于号
    pyautogui.moveTo(start_x, start_y)  # 移动到起始位置
    pyautogui.mouseDown()  # 按下鼠标
    pyautogui.moveTo(start_x - 50, start_y + 50, duration=0.001)  # 向上移动绘制第一条线
    pyautogui.moveTo(start_x, start_y + 100, duration=0.001)  # 向下移动绘制第二条线
    pyautogui.mouseUp()  # 松开鼠标


def main():
    keyboard.add_hotkey('=', lambda: sys.exit("进程已结束"))  # 默认的退出快捷键

    try:
        while True:
            # Capture the left and right areas separately
            left_image, right_image = capture_area()  # Capture the screen area and get two images
            
            # Recognize numbers from the left and right images
            numbers = recognize_numbers(left_image, right_image)
            
            # Compare and draw results
            draw_comparison(numbers)
            
            time.sleep(0.03)  # Add a small delay to prevent excessive loop speed
    except SystemExit as e:
        print(e)

if __name__ == "__main__":
    main()  # Start the main program

