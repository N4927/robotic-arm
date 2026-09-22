"""Autonomous object detection and grabbing for the Raspberry Pi robotic arm.

This is the most complete version preserved from the original project. It scans
with the base servo until the ultrasonic sensor detects an object, then moves
the arm and gripper through calibrated positions based on the measured distance.

Run `sudo pigpiod` before starting this script.
"""

import math
import time

import pygame
from gpiozero import DistanceSensor, Servo
from gpiozero.pins.pigpio import PiGPIOFactory


# Servo GPIO pins, using BCM numbering.
BASE_SERVO_PIN = 17
SHOULDER_SERVO_PIN = 12
ELBOW_SERVO_PIN = 24
GRIPPER_LEFT_SERVO_PIN = 25
GRIPPER_RIGHT_SERVO_PIN = 8

ECHO_PIN = 7
TRIGGER_PIN = 23

MANUAL_SPEED = 1


pygame.init()
factory = PiGPIOFactory()

base_servo = Servo(BASE_SERVO_PIN, pin_factory=factory)
shoulder_servo = Servo(SHOULDER_SERVO_PIN, pin_factory=factory)
elbow_servo = Servo(ELBOW_SERVO_PIN, pin_factory=factory)
gripper_left_servo = Servo(GRIPPER_LEFT_SERVO_PIN, pin_factory=factory)
gripper_right_servo = Servo(GRIPPER_RIGHT_SERVO_PIN, pin_factory=factory)

sensor = DistanceSensor(echo=ECHO_PIN, trigger=TRIGGER_PIN, pin_factory=factory)


def servo_value(angle_degrees):
    """Convert the project's calibrated angle value into a gpiozero servo value."""
    return math.sin(math.radians(angle_degrees))


def set_arm_position(base=None, shoulder=None, elbow=None, gripper_left=None, gripper_right=None):
    """Move any provided servos to their calibrated positions."""
    if base is not None:
        base_servo.value = servo_value(base)
    if shoulder is not None:
        shoulder_servo.value = servo_value(shoulder)
    if elbow is not None:
        elbow_servo.value = servo_value(elbow)
    if gripper_left is not None:
        gripper_left_servo.value = servo_value(gripper_left)
    if gripper_right is not None:
        gripper_right_servo.value = servo_value(gripper_right)


def read_distance_cm():
    """Read the ultrasonic distance sensor and return the distance in centimeters."""
    distance = round(sensor.distance * 100, 2)
    print("Distance:", distance, "cm")
    time.sleep(0.01)
    return distance


def manual_control():
    """Control the arm manually with number keys and the left/right arrows."""
    base = 440
    shoulder = 100
    elbow = 200
    gripper_left = 150
    gripper_right = 150

    set_arm_position(
        base=base,
        shoulder=shoulder,
        elbow=elbow,
        gripper_left=gripper_left,
        gripper_right=gripper_right,
    )

    selected_servo = 1
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
                if event.key == pygame.K_5:
                    selected_servo = 5

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
        if selected_servo == 5:
            time.sleep(1)
            read_distance_cm()

        window.fill((0, 0, 0))
        pygame.display.update()

        set_arm_position(
            base=base,
            shoulder=shoulder,
            elbow=elbow,
            gripper_left=gripper_left,
            gripper_right=gripper_right,
        )

    pygame.quit()


def autonomous_grab():
    """Scan for an object with the ultrasonic sensor and run the grab sequence."""
    base = 430
    shoulder = 100
    elbow = 200
    gripper_left = 150
    gripper_right = 150
    keep_scanning = True

    set_arm_position(
        shoulder=shoulder,
        elbow=elbow,
        gripper_left=gripper_left,
        gripper_right=gripper_right,
    )
    time.sleep(1)

    while keep_scanning:
        distance = read_distance_cm()

        if distance >= 20:
            base += 0.4
            set_arm_position(base=base)

        if distance < 20:
            set_arm_position(base=base)
            time.sleep(0.1)
            object_distance = read_distance_cm()
            time.sleep(0.1)
            object_distance = read_distance_cm()
            time.sleep(0.4)
            object_distance = read_distance_cm()
            time.sleep(0.4)
            object_distance = read_distance_cm()
            keep_scanning = False

    # Calibrated reach positions for the original fork/gripper length.
    if 19 <= object_distance < 21:
        print("21")
        shoulder = 164
        elbow = 197
    elif 17 <= object_distance < 20:
        print("19")
        shoulder = 159
        elbow = 194
    elif 14 <= object_distance < 17:
        print("16")
        shoulder = 154
        elbow = 187
    elif 11 <= object_distance < 14:
        print("13")
        shoulder = 150
        elbow = 182
    elif 8 <= object_distance < 11:
        print("10")
        shoulder = 144
        elbow = 178
    elif 5 <= distance < 8:
        print("6")
        shoulder = 134
        elbow = 174
    elif 3 <= object_distance < 5:
        print("5")
        shoulder = 134
        elbow = 168

    gripper_right = 180
    gripper_left = 120

    time.sleep(0.75)
    set_arm_position(shoulder=shoulder, elbow=elbow)
    time.sleep(1)
    set_arm_position(gripper_left=gripper_left, gripper_right=gripper_right)
    time.sleep(1.5)

    if (
        gripper_left_servo.value == servo_value(120)
        and gripper_right_servo.value == servo_value(180)
    ):
        reset_arm()
    else:
        set_arm_position(gripper_left=120, gripper_right=180)
        reset_arm()


def reset_arm():
    """Return the arm to the original resting position used by the prototype."""
    set_arm_position(shoulder=100)
    time.sleep(0.2)
    set_arm_position(elbow=200)
    time.sleep(1.5)
    set_arm_position(base=450)
    time.sleep(3.5)


if __name__ == "__main__":
    try:
        autonomous_grab()
        # manual_control()
    except KeyboardInterrupt:
        print("User stopped the program.")
