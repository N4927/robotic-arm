# Raspberry Pi Robotic Arm

A Python-based Raspberry Pi robotic arm project that controls multiple servo motors, supports manual keyboard movement, and uses an ultrasonic distance sensor for simple autonomous object detection and grabbing.

This repository is an archived high-school Matura project. It has been cleaned up for readability and portfolio presentation while preserving the original experimental iterations that were created during development.

The latest repository changes are organizational and documentation-focused. They are intended to make the project easier to understand for external viewers; they do not substantially change the original robotic-arm behavior.

## Academic Context

This project was originally developed as a high-school Matura work and received the maximum grade of 6.

- School year: 2021-2022
- Original report date: February 15, 2022
- School: Liceo Lugano 1
- Supervisor: Amedeo Mazzoleni
- Portfolio cleanup date: September 22, 2026
- Original report: [`docs/robotic-arm-report-IT.pdf`](docs/robotic-arm-report-IT.pdf)
- English translation: [`docs/robotic-arm-report-EN.pdf`](docs/robotic-arm-report-EN.pdf)

## Project Overview

The project explores basic hardware-software interaction with a small robotic arm. The Raspberry Pi controls five servo motors through GPIO, reads distance measurements from an ultrasonic sensor, and uses those measurements to decide when to stop scanning and perform a grabbing sequence.

The code is intentionally simple and reflects an iterative prototyping process: manual control was built first, ultrasonic sensing was added, and later versions combined scanning, distance-based calibration, and a gripper action.

## Features

- Manual servo control with a keyboard and Pygame
- Five-servo robotic arm control using Raspberry Pi GPIO
- Ultrasonic distance sensing
- Basic autonomous object detection
- Distance-band-based grabbing sequence
- Archived experimental versions showing the development history
- Early OpenCV color-tracking experiment preserved in the archive

## Hardware Used

- Raspberry Pi
- Multi-servo robotic arm
- Five servo motors
- Ultrasonic distance sensor, such as an HC-SR04-style module
- External servo power supply
- Jumper wires and breadboard/prototyping wiring

## Software and Technologies

- Python
- Raspberry Pi GPIO
- gpiozero
- pigpio / PiGPIOFactory for smoother servo control
- Pygame for keyboard input
- OpenCV and NumPy in archived vision experiments

## How the Robotic Arm Works

The arm uses calibrated numeric position values for each servo. These values are converted into `gpiozero.Servo` values using a sine-based mapping from the original project code. The main autonomous script starts the arm in a resting position, rotates the base while checking the ultrasonic sensor, and stops when an object is detected within a threshold distance.

After detection, the script takes several distance readings, chooses a calibrated shoulder/elbow position based on the measured range, closes the gripper, and then returns the arm toward its resting position.

## Manual Control

Manual control is implemented in `src/manual_control.py`. A small Pygame window captures keyboard input:

- `1`: select the base servo
- `2`: select the shoulder servo
- `3`: select the elbow servo
- `4`: select the gripper servo pair
- Left/Right arrows: move the selected servo or servo pair

This mode was useful for testing servo limits and manually finding the calibrated values later used by the autonomous mode.

## Ultrasonic Distance Sensing

The main autonomous version uses `gpiozero.DistanceSensor` with the trigger and echo GPIO pins defined in the source file. Earlier prototypes used raw `RPi.GPIO` pulse timing; those versions are preserved in `archive/`.

Distance readings are converted to centimeters and printed during execution so the calibration process can be observed from the terminal.

## Autonomous Object Detection and Grabbing

The autonomous controller in `src/autonomous_control.py` rotates the base until the ultrasonic sensor detects an object closer than approximately 20 cm. It then maps the measured distance to one of several hand-calibrated arm positions and closes the gripper.

This is a basic feedback-based control loop rather than a full robotics planning system. The value of the project is in the integration work: GPIO control, sensor feedback, servo calibration, debugging hardware behavior, and iterating from manual control toward autonomous movement.

## Repository Structure

```text
robotic-arm/
|-- README.md
|-- requirements.txt
|-- .gitignore
|-- docs/
|   |-- robotic-arm-report-IT.pdf
|   `-- robotic-arm-report-EN.pdf
|-- src/
|   |-- autonomous_control.py
|   `-- manual_control.py
`-- archive/
    |-- early_distance_scan_autonomous.py
    |-- combined_manual_autonomous_v1.py
    |-- combined_manual_autonomous_v2.py
    |-- inverse_kinematics_and_vision_experiment.py
    `-- color_tracking_experiment.py
```

## Reports

The repository includes the original Italian Matura report and an English translation prepared for portfolio use. These documents provide the academic context for the work and explain the original design process in more detail.

- [`robotic-arm-report-IT.pdf`](docs/robotic-arm-report-IT.pdf): original Italian report, titled "Il lampone informatico"
- [`robotic-arm-report-EN.pdf`](docs/robotic-arm-report-EN.pdf): English translation for portfolio readers

## Setup / Requirements

This project is intended to run on a Raspberry Pi connected to the robotic arm hardware.

1. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the pigpio daemon before running servo-control scripts:

   ```bash
   sudo pigpiod
   ```

3. Check the GPIO pin constants in the source files and adjust them if your wiring differs.

## How to Run

Run the main autonomous controller:

```bash
python src/autonomous_control.py
```

Run manual keyboard control:

```bash
python src/manual_control.py
```

The archive scripts are included for historical reference. They may require the same Raspberry Pi hardware setup and, for the vision experiments, a connected camera.

## What I Learned

- Controlling servo motors from Python on a Raspberry Pi
- Using GPIO libraries and understanding pin mappings
- Integrating an ultrasonic distance sensor into a control loop
- Calibrating physical motion through repeated testing
- Debugging hardware timing and sensor-read issues
- Building a manual control mode to support later autonomous behavior
- Iterating through prototypes and preserving earlier experiments for reference

## Project Status

Archived / completed high-school Matura learning project.

The repository has been cleaned for readability and portfolio use, but the core behavior and original experimental structure have been preserved. The latest modifications are presentation improvements for external viewers rather than a redesign of the original project.
