import time
import threading
import RPi.GPIO as GPIO
import asyncio

class ObstacleAvoidance:
    def __init__(self, trig_pin=27, echo_pin=22, loop=None):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin
        self.loop = loop
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def init_obstacle_thread(self, queue, motor):
        thread = threading.Thread(target=self.avoidance_thread, args=(queue, motor), daemon=True)
        thread.start()

    def get_ultrasonic_distance(self, num_readings=3):
        distances = []
        try:
            for _ in range(num_readings):
                GPIO.output(self.trig_pin, True)
                time.sleep(0.00001)
                GPIO.output(self.trig_pin, False)

                timeout = time.time() + 0.1
                while GPIO.input(self.echo_pin) == 0:
                    if time.time() > timeout:
                        return -1
                pulse_start = time.time()

                timeout = time.time() + 0.1
                while GPIO.input(self.echo_pin) == 1:
                    if time.time() > timeout:
                        return -1
                pulse_end = time.time()

                duration = pulse_end - pulse_start
                distances.append(round(duration * 17150, 2))

            return sum(distances) / len(distances)
        except Exception as e:
            print(f"[Ultrasonic Error] {e}")
            return -1

    def avoidance_thread(self, queue, motor):
        while True:
            distance = self.get_ultrasonic_distance()
            if 0 < distance < 15:
                print("[AVOIDANCE] Obstacle detected!")
                task = lambda: self.avoid_obstacle(motor)
                asyncio.run_coroutine_threadsafe(queue.put((0, task)), self.loop)
            time.sleep(0.2)

    def avoid_obstacle(self, motor):
        print("[AVOIDANCE] Avoiding...")
        motor.stop_car()
        time.sleep(0.1)
        motor.turn_right(speed=800)
        time.sleep(2)
        motor.stop_car()

    def check_and_avoid(self, motor):
        """Optional: Called from BLE to check and react instantly."""
        distance = self.get_ultrasonic_distance()
        if 0 < distance < 15:
            self.avoid_obstacle(motor)
            return True
        return False
