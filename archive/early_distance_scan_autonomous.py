"""Early autonomous distance-scanning prototype.

This version used raw RPi.GPIO timing for the ultrasonic sensor. It is preserved
as an archive because it documents an early problem in the project: once the
base servo started rotating, the nested movement loop prevented new distance
measurements from being read.
"""

import math
import time

import RPi.GPIO as GPIO
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory


TRIGGER_PIN = 23
ECHO_PIN = 18


GPIO.setwarnings(False)
factory = PiGPIOFactory()

base_servo = Servo(17, pin_factory=factory)
shoulder_servo = Servo(12, pin_factory=factory)
elbow_servo = Servo(24, pin_factory=factory)
gripper_left_servo = Servo(25, pin_factory=factory)
gripper_right_servo = Servo(8, pin_factory=factory)


def servo_value(angle_degrees):
    """Convert the project's calibrated angle value into a gpiozero servo value."""
    return math.sin(math.radians(angle_degrees))


def read_distance_cm():
    """Read the ultrasonic sensor with raw GPIO pulse timing."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIGGER_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

    GPIO.output(TRIGGER_PIN, False)
    time.sleep(1)

    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = round(pulse_duration * 17150, 2)

    print("Distance:", distance, "cm")
    return distance


def movement():
    """Scan with the base servo until the sensor sees an object."""
    base = 450
    shoulder = 100
    elbow = 200
    gripper_left = 150
    gripper_right = 150

    shoulder_servo.value = servo_value(shoulder)
    elbow_servo.value = servo_value(elbow)
    gripper_left_servo.value = servo_value(gripper_left)
    gripper_right_servo.value = servo_value(gripper_right)

    while True:
        distance = read_distance_cm()

        if distance >= 10:
            # Original early behavior: this inner loop blocks future reads.
            while True:
                base += 0.01
                base_servo.value = servo_value(base)

        elif distance < 10:
            base_servo.value = servo_value(base)


if __name__ == "__main__":
    movement()
