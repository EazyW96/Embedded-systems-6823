from picamera2 import Picamera2
import time
import os

save_path = "/home/ciaon/Embedded-systems-6823/ble_images"
os.makedirs(save_path, exist_ok=True)

camera = Picamera2()
camera.configure(camera.create_still_configuration())
camera.start()

print("?? Starting PiCamera2. Place your iPhone in view...")

for i in range(1, 31):
    filename = f"{save_path}/iphone_{i}.jpg"
    camera.capture_file(filename)
    print(f"? Saved: {filename}")
    time.sleep(1)

camera.stop()
print("?? Done taking all pictures!")
