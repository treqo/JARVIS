import os
from PIL import ImageGrab
def take_screenshot():
    path = os.path.join(os.path.dirname(__file__), '../assets/img/screenshot.jpg')
    screenshot = ImageGrab.grab()
    rgb_screenshot = screenshot.convert('RGB')
    rgb_screenshot.save(path, quality=15) # faster with low quality

take_screenshot()