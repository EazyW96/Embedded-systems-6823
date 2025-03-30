from picamera2 import Picamera2
import time
import os

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

# Photo capture loop
print("?? Starting photo capture. Taking 10 pictures every 5 seconds...")

for i in range(1, PHOTO_COUNT + 1):
    filename = os.path.join(SAVE_PATH, f"simple_photo_{i}.jpg")
    camera.capture_file(filename)
    print(f"? Saved photo {i}: {filename}")
    time.sleep(INTERVAL)

# Cleanup
camera.stop_preview()
camera.stop()
print("? Done taking pictures.")
