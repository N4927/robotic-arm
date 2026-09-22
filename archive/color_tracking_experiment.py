"""OpenCV green-object tracking experiment.

This standalone experiment estimates the center of a green object in the camera
frame and increments two position variables based on motion. It was not fully
integrated with the servo-control scripts.
"""

import cv2
import numpy as np


LOW_GREEN = np.array([45, 100, 115])
HIGH_GREEN = np.array([102, 255, 255])


def track_green_object():
    """Track a green object and print simple x/y movement counters."""
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


if __name__ == "__main__":
    track_green_object()
