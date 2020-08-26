import pyautogui
import time

print("move the mouse in 5 seconds")
time.sleep(5)
xy = pyautogui.position()
print(xy)
