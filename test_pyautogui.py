import pyautogui
import time
import logging

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_mouse_move():
    try:
        screen_width, screen_height = pyautogui.size()
        logging.info(f"屏幕分辨率: {screen_width}x{screen_height}")
        
        print("请将鼠标移动到屏幕左上角。测试将在3秒后开始。")
        time.sleep(3)
        
        # 移动到 (100, 100) 之前，确认这个位置不在屏幕角落
        target_x, target_y = 200, 200  # 根据屏幕分辨率调整
        logging.info(f"移动鼠标到 ({target_x}, {target_y})")
        
        pyautogui.moveTo(target_x, target_y, duration=1)
        pyautogui.click()
        print("鼠标移动和点击测试通过。")
    except pyautogui.FailSafeException:
        logging.error("Fail-safe 被触发！鼠标移动到屏幕角落以外的位置。")
        print("Fail-safe 被触发！请勿将鼠标移到屏幕角落。")
    except Exception as e:
        logging.error(f"pyautogui 测试出错: {e}")
        print("pyautogui 测试失败，请查看日志。")

if __name__ == "__main__":
    test_mouse_move()
