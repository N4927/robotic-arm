"""Inverse-kinematics and vision-tracking experiment.

This archived version explores three ideas beyond the main arm script:

1. Using a simple two-link inverse-kinematics calculation for the shoulder and
   elbow positions.
2. Writing servo coordinates to a CGI text file for a possible web interface.
3. Tracking a green object with OpenCV.

The project ultimately kept the hand-calibrated distance-band approach in
`src/autonomous_control.py`, but this file is preserved as part of the original
development history.
"""

import math
import time

import cv2
import numpy as np
import pygame
from gpiozero import DistanceSensor, Servo
from gpiozero.pins.pigpio import PiGPIOFactory


# This experiment used GPIO 27 for the base servo instead of GPIO 17.
BASE_SERVO_PIN = 27
SHOULDER_SERVO_PIN = 12
ELBOW_SERVO_PIN = 24
GRIPPER_LEFT_SERVO_PIN = 25
GRIPPER_RIGHT_SERVO_PIN = 8

ECHO_PIN = 7
TRIGGER_PIN = 23
MANUAL_SPEED = 1

LOW_GREEN = np.array([45, 100, 115])
HIGH_GREEN = np.array([102, 255, 255])


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

    window = pygame.display.set_mode((1, 1))
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

        base_servo.value = servo_value(base)
        shoulder_servo.value = servo_value(shoulder)
        elbow_servo.value = servo_value(elbow)
        gripper_left_servo.value = servo_value(gripper_left)
        gripper_right_servo.value = servo_value(gripper_right)

    pygame.quit()


def read_distance_cm():
    """Read the ultrasonic distance sensor and return centimeters."""
    distance = round(sensor.distance * 100, 2)
    print("Distance:", distance, "cm")
    time.sleep(0.01)
    return distance


def autonomous_grab_inverse_kinematics():
    """Scan for an object and calculate shoulder/elbow positions with IK."""
    gripper_left = 150
    gripper_right = 150
    base = 430
    shoulder = 100
    elbow = 200
    keep_scanning = True

    first_arm_length = 25
    second_arm_length = 32.5

    shoulder_servo.value = servo_value(shoulder)
    elbow_servo.value = servo_value(elbow)
    gripper_left_servo.value = servo_value(gripper_left)
    gripper_right_servo.value = servo_value(gripper_right)
    time.sleep(1)

    while keep_scanning:
        distance = read_distance_cm()

        if distance >= 20:
            base += 0.4
            base_servo.value = servo_value(base)

        if distance < 20:
            base_servo.value = servo_value(base)
            time.sleep(0.1)
            object_distance = read_distance_cm()
            time.sleep(0.1)
            object_distance = read_distance_cm()
            time.sleep(0.4)
            object_distance = read_distance_cm()
            time.sleep(0.4)
            object_distance = read_distance_cm()
            keep_scanning = False

    object_distance = object_distance + 3
    alpha = math.acos(
        (object_distance**2 + first_arm_length**2 - second_arm_length**2)
        / (2 * object_distance * second_arm_length)
    )
    beta = math.acos(
        (second_arm_length**2 + first_arm_length**2 - object_distance**2)
        / (2 * first_arm_length * second_arm_length)
    )

    print(alpha)
    print(beta)
    print(math.degrees(alpha))
    print(beta)
    print(math.radians(360 - math.degrees(alpha)))
    print(math.degrees(beta))

    shoulder_servo.value = math.sin(360 - math.radians(math.degrees(alpha)))
    elbow_servo.value = math.sin(math.radians(155 + math.degrees(beta)))

    time.sleep(0.5)
    gripper_right = 185
    gripper_left = 106
    gripper_left_servo.value = servo_value(gripper_left)
    gripper_right_servo.value = servo_value(gripper_right)
    time.sleep(1.5)

    shoulder_servo.value = servo_value(100)
    time.sleep(0.2)
    elbow_servo.value = servo_value(200)
    time.sleep(1.5)
    base_servo.value = servo_value(450)


def write_web_control_file():
    """Write starting servo positions to the original CGI text-file location."""
    base = 430
    shoulder = 100
    elbow = 200
    gripper_left = 150
    gripper_right = 150

    with open("/usr/lib/cgi-bin/dati.txt", "w", encoding="utf-8") as data_file:
        data_file.write("%s\n" % str(base))
        data_file.write("%s\n" % str(shoulder))
        data_file.write("%s\n" % str(elbow))
        data_file.write("%s\n" % str(gripper_left))
        data_file.write("%s\n" % str(gripper_right))

    ip_address = "172.20.10.3"
    print("For remote arm control, go to", ip_address, "from your device.")


def hand_tracking_experiment():
    """Track a green object and update two position counters."""
    horizontal_position = 100
    vertical_position = 100
    previous_x = 200
    previous_y = 150

    camera = cv2.VideoCapture(0)

    while True:
        _, frame = camera.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        green_mask = cv2.inRange(hsv_frame, LOW_GREEN, HIGH_GREEN)
        masked_frame = cv2.bitwise_and(frame, frame, mask=green_mask)

        cv2.imshow("Frame", frame)
        cv2.imshow("Green mask", masked_frame)

        points = cv2.findNonZero(green_mask)
        if points is not None:
            average = np.mean(points, axis=0)
            average_2d = np.array(average)
            average_1d = average_2d[0]
            average_string = str(average_1d)
            digits = "".join(character for character in average_string if character.isdigit())

            x_string = digits[: len(digits) // 2]
            y_string = digits[len(digits) // 2 :]

            if len(x_string) >= 3 and len(y_string) >= 3:
                x_position = int(x_string[:3])
                y_position = int(y_string[:3])

                if x_position > previous_x:
                    horizontal_position += 1
                    previous_x = x_position
                elif x_position < previous_x:
                    horizontal_position -= 1
                    previous_x = x_position

                if y_position > previous_y:
                    vertical_position += 1
                    previous_y = y_position
                elif y_position < previous_y:
                    vertical_position -= 1
                    previous_y = y_position

        print(horizontal_position, vertical_position)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


base_servo.value = servo_value(430)
shoulder_servo.value = servo_value(100)
elbow_servo.value = servo_value(200)
gripper_left_servo.value = servo_value(150)
gripper_right_servo.value = servo_value(150)


if __name__ == "__main__":
    autonomous_grab_inverse_kinematics()
