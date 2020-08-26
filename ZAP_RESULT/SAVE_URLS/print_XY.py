import pyautogui
import time

print("move the mouse in 3 seconds")
time.sleep(3)
xy = pyautogui.position()
print(xy)
