from picamera2 import Picamera2
import time
import os
from datetime import datetime

# === Config ===
PHOTO_COUNT = 10
INTERVAL = 5  # Seconds between photos
SAVE_PATH = "/home/ciaon/Embedded-systems-6823/ble_images"

# Create folder if it doesn't exist
os.makedirs(SAVE_PATH, exist_ok=True)

# Setup camera
camera = Picamera2()
camera.configure(camera.create_still_configuration())
camera.start_preview()
camera.start()
time.sleep(2)  # Camera warm-up

print("?? Starting photo capture. Taking 10 pictures every 5 seconds...")

# Photo capture loop
for i in range(1, PHOTO_COUNT + 1):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(SAVE_PATH, f"ble_photo_{timestamp}.jpg")
    camera.capture_file(filename)
    print(f"? Saved photo {i}: {filename}")
    time.sleep(INTERVAL)

# Cleanup
camera.stop_preview()
camera.stop()
print("? Done taking pictures.")
