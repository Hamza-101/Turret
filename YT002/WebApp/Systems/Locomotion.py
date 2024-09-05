# try-catch code to check if motors work on startup  

import RPi.GPIO as GPIO
import time
import sys
import tty
import termios

class StepperMotorController:
    def __init__(self, step_pin, dir_pin, enable_pin):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        self.enable_pin = enable_pin
        self.step_delay = 0.001  # Delay between steps (in seconds)

        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.setup(self.enable_pin, GPIO.OUT)
        GPIO.output(self.enable_pin, GPIO.LOW)  # Enable motor

    def step_motor(self, direction):
        """Move the motor by one step in a specified direction."""
        GPIO.output(self.dir_pin, direction)
        GPIO.output(self.step_pin, GPIO.HIGH)
        time.sleep(self.step_delay)
        GPIO.output(self.step_pin, GPIO.LOW)
        time.sleep(self.step_delay)

    def move(self, direction):
        """Move the motor by one step."""
        self.step_motor(direction)

    def cleanup(self):
        """Disable motor and cleanup GPIO."""
        GPIO.output(self.enable_pin, GPIO.HIGH)  # Disable motor
        GPIO.cleanup()

class MotorControl:
    def __init__(self):
        # Initialize motors
        self.x_motor = StepperMotorController(step_pin=17, dir_pin=27, enable_pin=22)
        self.y_motor = StepperMotorController(step_pin=23, dir_pin=24, enable_pin=25)

    def get_key(self):
        """Get a single key press from the terminal."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    def run(self):
        """Main loop to control motors based on key presses."""
        try:
            print("Control motors using keys:")
            print("X-axis: 'a' to move left, 'd' to move right")
            print("Y-axis: 'w' to move up, 's' to move down")
            print("Press 'q' to quit")
            
            while True:
                key = self.get_key()
                
                if key == 'q':
                    break
                elif key == 'a':
                    self.x_motor.move(GPIO.LOW)  # Move X-axis left
                elif key == 'd':
                    self.x_motor.move(GPIO.HIGH)  # Move X-axis right
                elif key == 'w':
                    self.y_motor.move(GPIO.HIGH)  # Move Y-axis up
                elif key == 's':
                    self.y_motor.move(GPIO.LOW)  # Move Y-axis down
                else:
                    print("Invalid key. Use 'a', 'd', 'w', 's' or 'q'.")
        finally:
            # Cleanup
            self.x_motor.cleanup()
            self.y_motor.cleanup()

if __name__ == '__main__':
    controller = MotorControl()
    controller.run()
