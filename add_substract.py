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
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # 设置 Tesseract-OCR 的路径

# 跟踪状态的变量
not_found_count = 0
last_not_found_time = 0
last_numbers = None  # 存储上次识别的数字
skip_count = 0  # 跳过次数计数器

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
    region_relative = (214, 331, 148, 51)
    x, y = window_xy()
    # Calculate absolute screen coordinates
    region_absolute = (
        x + region_relative[0],
        y + region_relative[1],
        region_relative[2],
        region_relative[3]
    )
    
    # Take a screenshot
    screenshot = pyautogui.screenshot(region=region_absolute)
    image = np.array(screenshot)
    image_path = os.path.join(SCREENSHOT_DIR, "add_substract.png")
    # 将图像从RGB转换为BGR，以便与OpenCV兼容
    bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # 保存图像
    cv2.imwrite(image_path, bgr)
    # Return both images as a tuple
    return image


def recognize_numbers(image):
    # Convert both images to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # gray_left = cv2.resize(gray_left, (0, 0), fx=0.5, fy=0.5)
    # gray_right = cv2.resize(gray_right, (0, 0), fx=0.5, fy=0.5)

    # Apply thresholding to both images (use only the second value from cv2.threshold)
    _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789+-'

    # Recognize numbers in both the left and right images
    text = pytesseract.image_to_string(thresh, config=custom_config)

    # text = text.replace('A', '4')

    text = re.sub(r'[^0-9+\-]', '', text)


    print(f"Raw recognized text : {text}")

    return text

def calculate_expression(expr):
    # """
    # 使用 eval 计算数学表达式的结果。
    # 仅支持加减运算。
    # """
    try:
        # 确保表达式仅包含数字和加减号
        if re.fullmatch(r'[0-9+\-]+', expr):
            result = eval(expr)
            return result
        else:
            print(f"Invalid characters in expression: {expr}")
            return None
    except Exception as e:
        print(f"Error calculating expression '{expr}': {e}")
        return None

def handle_insufficient_numbers():
    global not_found_count, last_not_found_time

    current_time = time.time()
    not_found_count = not_found_count + 1 if current_time - last_not_found_time <= 1 else 1
    last_not_found_time = current_time

    print("Not enough numbers found for comparison")
    if not_found_count >= 25:
        click_buttons()
        time.sleep(9)
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

def draw_addsubstr(expression):
    global not_found_count, last_numbers, skip_count

    if not expression:
        handle_insufficient_numbers()
        return

    if last_expression is not None and last_expression == expression:
        skip_count += 1
        print(f"当前结果与上次相同，跳过此次执行（计数: {skip_count}）")
        if skip_count > 5:  # 如果跳过计数超过5，强制执行
            skip_count = 0
            execute_drawing_logic(expression)
        return
    
    # 计算表达式结果
    result = calculate_expression(expression)
    if result is None:
        handle_insufficient_numbers()
        return
    
    execute_drawing_logic(result)  # 执行当前数字的绘制逻辑

    not_found_count = 0  # 重置未找到计数
    last_expression = expression  # 更新上次识别的数字
    skip_count = 0  # 重置跳过次数

def extract_digits(number):
       
    if  (number > 999):
        raise ValueError("数字必须是三位数及以内")
    
    units = number % 10
    tens = (number // 10) % 10 if number >= 10 else None
    hundreds = (number // 100) % 10 if number >= 100 else None
    
    return units, tens, hundreds

number_to_function = {
    0: draw_number_0,
    1: draw_number_1,
    2: draw_number_2,
    3: draw_number_3,
    4: draw_number_4,
    5: draw_number_5,
    6: draw_number_6,
    7: draw_number_7,
    8: draw_number_8,
    9: draw_number_9
}

def draw_number_0():
    pyautogui.mouseDown()  # 按下鼠标
    pyautogui.moveRel(-75, 120, duration=0.001)
    pyautogui.moveRel(75, 120, duration=0.001)
    pyautogui.moveRel(75, -120, duration=0.001)
    pyautogui.moveRel(-75, -120, duration=0.001)
    pyautogui.mouseUp()  # 松开鼠标

def execute_drawing_logic(result):
 
    print(f"result: {result}")

    units, tens, hundreds=extract_digits(result)

    x,y=window_xy()
    hundreds_x,hundreds_y=138,840
    tens_x,tens_y=332,840
    units_x,units_y=536,840

    if hundreds is not None:
        pyautogui.moveTo(x+hundreds_x, y+hundreds_y)
        func = number_to_function.get(hundreds)
        if func:
            func()
            time.sleep(0.01)  # 添加延迟以避免操作过快
    
    if tens is not None:
        pyautogui.moveTo(x+tens_x, y+tens_y)
        func = number_to_function.get(tens)
        if func:
            func()
            time.sleep(0.01)  # 添加延迟以避免操作过快

    if units is not None:
        pyautogui.moveTo(x+units_x, y+units_y)
        func = number_to_function.get(units)
        if func:
            func()
            time.sleep(0.01)  # 添加延迟以避免操作过快




def main():
    keyboard.add_hotkey('=', lambda: sys.exit("进程已结束"))  # 默认的退出快捷键

    try:
        while True:
            image = capture_area()  # 截取屏幕区域
            numbers = recognize_numbers(image)  # 从截取的图像中识别数字
            draw_comparison(numbers)  # 比较并绘制结果
           # time.sleep(0.01)
    except SystemExit as e:
        print(e)

if __name__ == "__main__":
    main()  # 启动主程序