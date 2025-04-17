import time
from modules.servo_control import Servo
from modules.pca9685 import PCA9685

class MotorControl:
    def __init__(self):
        self.pwm = PCA9685(0x40, debug=True)
        self.pwm.set_pwm_freq(50)
        
    def duty_range(self,duty1,duty2,duty3,duty4):
        if duty1>4095:
            duty1=4095
        elif duty1<-4095:
            duty1=-4095        
        
        if duty2>4095:
            duty2=4095
        elif duty2<-4095:
            duty2=-4095
            
        if duty3>4095:
            duty3=4095
        elif duty3<-4095:
            duty3=-4095
            
        if duty4>4095:
            duty4=4095
        elif duty4<-4095:
            duty4=-4095
        return duty1,duty2,duty3,duty4
        
    def left_Upper_Wheel(self,duty):
        if duty>0:
            self.pwm.set_motor_pwm(0,0)
            self.pwm.set_motor_pwm(1,duty)
        elif duty<0:
            self.pwm.set_motor_pwm(1,0)
            self.pwm.set_motor_pwm(0,abs(duty))
        else:
            self.pwm.set_motor_pwm(0,4095)
            self.pwm.set_motor_pwm(1,4095)
            
    def left_Lower_Wheel(self,duty):
        if duty>0:
            self.pwm.set_motor_pwm(3,0)
            self.pwm.set_motor_pwm(2,duty)
        elif duty<0:
            self.pwm.set_motor_pwm(2,0)
            self.pwm.set_motor_pwm(3,abs(duty))
        else:
            self.pwm.set_motor_pwm(2,4095)
            self.pwm.set_motor_pwm(3,4095)
            
    def right_Upper_Wheel(self,duty):
        if duty>0:
            self.pwm.set_motor_pwm(6,0)
            self.pwm.set_motor_pwm(7,duty)
        elif duty<0:
            self.pwm.set_motor_pwm(7,0)
            self.pwm.set_motor_pwm(6,abs(duty))
        else:
            self.pwm.set_motor_pwm(6,4095)
            self.pwm.set_motor_pwm(7,4095)
            
    def right_Lower_Wheel(self,duty):
        if duty>0:
            self.pwm.set_motor_pwm(4,0)
            self.pwm.set_motor_pwm(5,duty)
        elif duty<0:
            self.pwm.set_motor_pwm(5,0)
            self.pwm.set_motor_pwm(4,abs(duty))
        else:
            self.pwm.set_motor_pwm(4,4095)
            self.pwm.set_motor_pwm(5,4095)
 
    def setMotorModel(self,duty1,duty2,duty3,duty4):
        duty1,duty2,duty3,duty4=self.duty_range(duty1,duty2,duty3,duty4)
        self.left_Upper_Wheel(duty1)
        self.left_Lower_Wheel(duty2)
        self.right_Upper_Wheel(duty3)
        self.right_Lower_Wheel(duty4)

    def move_forward(self, speed=50):
        print("Moving forward...")
        self.setMotorModel(2000, 2000, 2000, 2000)

    def move_backwards(self, speed=50):
        print("Moving backward...")
        self.setMotorModel(-2000,-2000,-2000,-2000)

    def turn_left(self, speed=25):
        print("Turning left...")
        self.setMotorModel(-500,-500,2000,2000) 

    def turn_right(self, speed=25):
        print("Turning right...")
        self.setMotorModel(1000,2000,-500,-500)

    def stop_car(self):
        print("Stopping car.")
        self.setMotorModel(0,0,0,0)

    def set_servo_angle(self, channel: str, angle: int, error: int = 10):
        self.servo.set_servo_angle(channel, angle, error)

    def cleanup(self):
        print("Motor cleanup ...")
        self.stop_car()
