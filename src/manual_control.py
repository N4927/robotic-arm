"""Manual keyboard control for the Raspberry Pi robotic arm.

Run `sudo pigpiod` before starting this script.

Controls:
    1-4: select the motor/group to control
    Left/Right arrows: move the selected motor/group
"""

import math

import pygame
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory


BASE_SERVO_PIN = 17
SHOULDER_SERVO_PIN = 12
ELBOW_SERVO_PIN = 24
GRIPPER_LEFT_SERVO_PIN = 25
GRIPPER_RIGHT_SERVO_PIN = 8

STEP_SIZE = 3


pygame.init()
window = pygame.display.set_mode((500, 500))

factory = PiGPIOFactory()

base_servo = Servo(BASE_SERVO_PIN, pin_factory=factory)
shoulder_servo = Servo(SHOULDER_SERVO_PIN, pin_factory=factory)
elbow_servo = Servo(ELBOW_SERVO_PIN, pin_factory=factory)
gripper_left_servo = Servo(GRIPPER_LEFT_SERVO_PIN, pin_factory=factory)
gripper_right_servo = Servo(GRIPPER_RIGHT_SERVO_PIN, pin_factory=factory)


def servo_value(angle_degrees):
    """Convert the project's calibrated angle value into a gpiozero servo value."""
    return math.sin(math.radians(angle_degrees))


def set_arm_position(base, shoulder, elbow, gripper_left, gripper_right):
    """Send the current calibrated positions to the five servos."""
    base_servo.value = servo_value(base)
    shoulder_servo.value = servo_value(shoulder)
    elbow_servo.value = servo_value(elbow)
    gripper_left_servo.value = servo_value(gripper_left)
    gripper_right_servo.value = servo_value(gripper_right)


def manual_control():
    """Control each servo with a simple Pygame keyboard window."""
    base = 440
    shoulder = 100
    elbow = 200
    gripper_left = 150
    gripper_right = 150
    selected_servo = 1

    running = True
    while running:
        pygame.time.delay(100)

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
                base += STEP_SIZE
                if base > 440:
                    base = 440
            if keys[pygame.K_RIGHT]:
                base -= STEP_SIZE
                if base < 290:
                    base = 290

        if selected_servo == 2:
            if keys[pygame.K_LEFT]:
                shoulder += STEP_SIZE
                if shoulder > 180:
                    shoulder = 180
            if keys[pygame.K_RIGHT]:
                shoulder -= STEP_SIZE
                if shoulder < 85:
                    shoulder = 85

        if selected_servo == 3:
            if keys[pygame.K_LEFT]:
                elbow += STEP_SIZE
                if elbow > 360:
                    elbow = 360
            if keys[pygame.K_RIGHT]:
                elbow -= STEP_SIZE
                if elbow < 0:
                    elbow = 0

        if selected_servo == 4:
            if keys[pygame.K_LEFT]:
                gripper_right -= STEP_SIZE
                gripper_left += STEP_SIZE
                if gripper_left > 185:
                    gripper_left = 185
                if gripper_right < 115:
                    gripper_right = 115
            if keys[pygame.K_RIGHT]:
                gripper_right += STEP_SIZE
                gripper_left -= STEP_SIZE
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

        set_arm_position(base, shoulder, elbow, gripper_left, gripper_right)

    pygame.quit()


if __name__ == "__main__":
    manual_control()
