"""First combined manual/autonomous robotic-arm prototype.

This iteration includes keyboard control and a raw GPIO ultrasonic-distance
reader. The autonomous mode scans until an object is within 20 cm, then moves to
one of several hand-calibrated grab positions.
"""

import math
import time

import pygame
import RPi.GPIO as GPIO
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory


TRIGGER_PIN = 23
ECHO_PIN = 18
MANUAL_SPEED = 1


pygame.init()
factory = PiGPIOFactory()

base_servo = Servo(17, pin_factory=factory)
shoulder_servo = Servo(12, pin_factory=factory)
elbow_servo = Servo(24, pin_factory=factory)
gripper_left_servo = Servo(25, pin_factory=factory)
gripper_right_servo = Servo(8, pin_factory=factory)


def servo_value(angle_degrees):
    """Convert the project's calibrated angle value into a gpiozero servo value."""
    return math.sin(math.radians(angle_degrees))


def manual_control():
    """Manual control with number keys selecting the active servo."""
    base = 440
    shoulder = 100
    elbow = 200
    gripper_left = 150
    gripper_right = 150
    selected_servo = 1

    base_servo.value = servo_value(base)
    shoulder_servo.value = servo_value(shoulder)
    elbow_servo.value = servo_value(elbow)
    gripper_left_servo.value = servo_value(gripper_left)
    gripper_right_servo.value = servo_value(gripper_right)

    window = pygame.display.set_mode((500, 500))
    running = True

    while running:
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_servo = 1
                if event.key == pygame.K_2:
                    selected_servo = 2
                if event.key == pygame.K_3:
                    selected_servo = 3
                if event.key == pygame.K_4:
                    selected_servo = 4

        keys = pygame.key.get_pressed()

        if selected_servo == 1:
            if keys[pygame.K_LEFT]:
                base += MANUAL_SPEED
                if base > 440:
                    base = 440
            if keys[pygame.K_RIGHT]:
                base -= MANUAL_SPEED
                if base < 290:
                    base = 290

        if selected_servo == 2:
            if keys[pygame.K_LEFT]:
                shoulder += MANUAL_SPEED
                if shoulder > 180:
                    shoulder = 180
            if keys[pygame.K_RIGHT]:
                shoulder -= MANUAL_SPEED
                if shoulder < 85:
                    shoulder = 85

        if selected_servo == 3:
            if keys[pygame.K_LEFT]:
                elbow += MANUAL_SPEED
                if elbow > 360:
                    elbow = 360
            if keys[pygame.K_RIGHT]:
                elbow -= MANUAL_SPEED
                if elbow < 0:
                    elbow = 0

        if selected_servo == 4:
            if keys[pygame.K_LEFT]:
                gripper_right -= MANUAL_SPEED
                gripper_left += MANUAL_SPEED
                if gripper_left > 185:
                    gripper_left = 185
                if gripper_right < 115:
                    gripper_right = 115
            if keys[pygame.K_RIGHT]:
                gripper_right += MANUAL_SPEED
                gripper_left -= MANUAL_SPEED
                if gripper_left < 105:
                    gripper_left = 105
                if gripper_right > 185:
                    gripper_right = 185

        if selected_servo == 1:
            print(base)
        if selected_servo == 2:
            print(shoulder)
        if selected_servo == 3:
            print(elbow)
        if selected_servo == 4:
            print(gripper_left)
            print("-------")
            print(gripper_right)

        window.fill((0, 0, 0))
        pygame.display.update()

        base_servo.value = servo_value(base)
        shoulder_servo.value = servo_value(shoulder)
        elbow_servo.value = servo_value(elbow)
        gripper_left_servo.value = servo_value(gripper_left)
        gripper_right_servo.value = servo_value(gripper_right)

    pygame.quit()


def read_distance_cm():
    """Read the ultrasonic sensor with raw GPIO pulse timing."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(TRIGGER_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

    GPIO.output(TRIGGER_PIN, False)
    time.sleep(0.1)

    GPIO.output(TRIGGER_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIGGER_PIN, False)

    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    return round(pulse_duration * 17150, 2)


def autonomous_grab():
    """Scan and run the first hand-calibrated grabbing sequence."""
    base = 440
    shoulder = 100
    elbow = 200
    gripper_left = 150
    gripper_right = 150
    keep_scanning = True

    shoulder_servo.value = servo_value(shoulder)
    elbow_servo.value = servo_value(elbow)
    gripper_left_servo.value = servo_value(gripper_left)
    gripper_right_servo.value = servo_value(gripper_right)

    while keep_scanning:
        distance = read_distance_cm()

        if distance >= 20:
            base += 2.2
            base_servo.value = servo_value(base)

        if distance < 20:
            base_servo.value = servo_value(base)
            keep_scanning = False

    if 15 <= distance < 20:
        shoulder = 166
        elbow = 191
        gripper_left = 105
        gripper_right = 185
    elif 12 <= distance < 15:
        shoulder = 161
        elbow = 188
        gripper_left = 105
        gripper_right = 185
    elif 8 <= distance < 12:
        shoulder = 151
        elbow = 179
        gripper_left = 105
        gripper_right = 185
    elif 4 <= distance < 8:
        shoulder = 145
        elbow = 167
        gripper_left = 105
        gripper_right = 185

    shoulder_servo.value = servo_value(shoulder)
    time.sleep(0.5)
    elbow_servo.value = servo_value(elbow)
    time.sleep(0.75)
    gripper_left_servo.value = servo_value(gripper_left)
    gripper_right_servo.value = servo_value(gripper_right)
    time.sleep(1)

    shoulder_servo.value = servo_value(100)
    elbow_servo.value = servo_value(200)
    time.sleep(1.5)
    base_servo.value = servo_value(450)
    time.sleep(3.5)


if __name__ == "__main__":
    autonomous_grab()
    # manual_control()
