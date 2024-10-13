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
import logging

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
    print(f"BlueStacks window position: ({window_x}, {window_y})")  # 添加此行

    return window_x, window_y



def extract_digits(number):
       
    if  (number > 999):
        raise ValueError("数字必须是三位数及以内")
    
    units = number % 10
    tens = (number // 10) % 10 if number >= 10 else None
    hundreds = (number // 100) % 10 if number >= 100 else None
    
    return units, tens, hundreds


def draw_number_0():
    try:
        logging.info("执行操作：绘制 '0'")
        pyautogui.mouseDown()  # 按下鼠标
        pyautogui.moveRel(-75, 120, duration=0.1)
        pyautogui.moveRel(75, 120, duration=0.1)
        pyautogui.moveRel(75, -120, duration=0.1)
        pyautogui.moveRel(-75, -120, duration=0.1)
        pyautogui.mouseUp()  # 松开鼠标
        logging.info("完成绘制 '0'")
    except Exception as e:
        logging.error(f"绘制 '0' 时出错: {e}")


def draw_number_1():
    pyautogui.mouseDown()  # 按下鼠标
    pyautogui.moveRel(-75, 120, duration=0.001)
    pyautogui.moveRel(75, 120, duration=0.001)
    pyautogui.moveRel(75, -120, duration=0.001)
    pyautogui.moveRel(-75, -120, duration=0.001)
    pyautogui.mouseUp()  # 松开鼠标

def draw_number_2():
    pyautogui.mouseDown()  # 按下鼠标
    pyautogui.moveRel(-75, 120, duration=0.001)
    pyautogui.moveRel(75, 120, duration=0.001)
    pyautogui.moveRel(75, -120, duration=0.001)
    pyautogui.moveRel(-75, -120, duration=0.001)
    pyautogui.mouseUp()  # 松开鼠标

def draw_number_3():
    pyautogui.mouseDown()  # 按下鼠标
    pyautogui.moveRel(-75, 120, duration=0.001)
    pyautogui.moveRel(75, 120, duration=0.001)
    pyautogui.moveRel(75, -120, duration=0.001)
    pyautogui.moveRel(-75, -120, duration=0.001)
    pyautogui.mouseUp()  # 松开鼠标

def draw_number_4():
    pyautogui.mouseDown()  # 按下鼠标
    pyautogui.moveRel(-75, 120, duration=0.001)
    pyautogui.moveRel(75, 120, duration=0.001)
    pyautogui.moveRel(75, -120, duration=0.001)
    pyautogui.moveRel(-75, -120, duration=0.001)
    pyautogui.mouseUp()  # 松开鼠标

def draw_number_5():
    pyautogui.mouseDown()  # 按下鼠标
    pyautogui.moveRel(-75, 120, duration=0.001)
    pyautogui.moveRel(75, 120, duration=0.001)
    pyautogui.moveRel(75, -120, duration=0.001)
    pyautogui.moveRel(-75, -120, duration=0.001)
    pyautogui.mouseUp()  # 松开鼠标

def draw_number_6():
    pyautogui.mouseDown()  # 按下鼠标
    pyautogui.moveRel(-75, 120, duration=0.001)
    pyautogui.moveRel(75, 120, duration=0.001)
    pyautogui.moveRel(75, -120, duration=0.001)
    pyautogui.moveRel(-75, -120, duration=0.001)
    pyautogui.mouseUp()  # 松开鼠标

def draw_number_7():
    pyautogui.mouseDown()  # 按下鼠标
    pyautogui.moveRel(-75, 120, duration=0.001)
    pyautogui.moveRel(75, 120, duration=0.001)
    pyautogui.moveRel(75, -120, duration=0.001)
    pyautogui.moveRel(-75, -120, duration=0.001)
    pyautogui.mouseUp()  # 松开鼠标

def draw_number_8():
    pyautogui.mouseDown()  # 按下鼠标
    pyautogui.moveRel(-75, 120, duration=0.001)
    pyautogui.moveRel(75, 120, duration=0.001)
    pyautogui.moveRel(75, -120, duration=0.001)
    pyautogui.moveRel(-75, -120, duration=0.001)
    pyautogui.mouseUp()  # 松开鼠标

def draw_number_9():
    pyautogui.mouseDown()  # 按下鼠标
    pyautogui.moveRel(-75, 120, duration=0.001)
    pyautogui.moveRel(75, 120, duration=0.001)
    pyautogui.moveRel(75, -120, duration=0.001)
    pyautogui.moveRel(-75, -120, duration=0.001)
    pyautogui.mouseUp()  # 松开鼠标

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


def execute_drawing_logic(result):
 
    print(f"result: {result}")

    units, tens, hundreds=extract_digits(result)
    print(f"digits: {extract_digits(result)}")
    
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
    while True:
        try:
            user_input = input("请输入一个三位数及以内的整数（或输入 'exit' 退出）： ")
            
            number = int(user_input)
            x,y=window_xy()
            pyautogui.moveTo(x+100, y+100)
            pyautogui.click()

         
            execute_drawing_logic(number)
            print(f"已执行数字 {number} 的绘制。\n")
        

        except KeyboardInterrupt:
            print("\n检测到键盘中断。退出程序。")
            break


if __name__ == "__main__":
    main()