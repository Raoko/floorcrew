#!/usr/bin/env python3
"""
FloorCrew Escort Bot — Person-Following Robot
Hackathon March 2026 | CoreWeave DCT

Pi 5 + Freenove 4WD + TFLite MobileNet SSD v2
Follows a person (vendor) on the DC floor autonomously.
"""

import time
import numpy as np
from picamera2 import Picamera2
from gpiozero import Robot, DistanceSensor
from tflite_runtime.interpreter import Interpreter

# ─── CONFIG ────────────────────────────────────────────────────────
MODEL_PATH = "models/ssd_mobilenet_v2.tflite"
LABELS_PATH = "models/coco_labels.txt"
PERSON_CLASS_ID = 0          # COCO class 0 = person
CONFIDENCE_THRESHOLD = 0.5   # Min detection confidence
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
INPUT_SIZE = (300, 300)      # MobileNet SSD input size

# Motor GPIO pins (BCM) — adjust to your Freenove wiring
LEFT_MOTOR = (17, 27)       # (forward, backward)
RIGHT_MOTOR = (22, 23)      # (forward, backward)

# Ultrasonic sensor pins (BCM)
ULTRASONIC_ECHO = 24
ULTRASONIC_TRIG = 25

# Steering
KP = 1.0                    # Proportional gain — tune on the floor
BASE_SPEED = 0.5            # 0.0–1.0
STOP_DISTANCE = 0.30        # meters — stop if obstacle closer than this
TARGET_AREA_RATIO = 0.15    # target bbox area / frame area (how close to follow)
AREA_TOLERANCE = 0.05       # dead zone around target area
LOST_TIMEOUT = 1.5          # seconds with no detection before stopping

# ─── SETUP ─────────────────────────────────────────────────────────

def load_labels(path):
    """Load COCO label map."""
    with open(path, "r") as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}


def init_camera():
    """Initialize Pi Camera with picamera2."""
    cam = Picamera2()
    config = cam.create_preview_configuration(
        main={"size": (FRAME_WIDTH, FRAME_HEIGHT), "format": "RGB888"}
    )
    cam.configure(config)
    cam.start()
    time.sleep(1)  # warm-up
    return cam


def init_tflite(model_path):
    """Load TFLite model and allocate tensors."""
    interpreter = Interpreter(model_path=model_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter, input_details, output_details


def init_robot():
    """Initialize motors and ultrasonic sensor."""
    robot = Robot(left=LEFT_MOTOR, right=RIGHT_MOTOR)
    sonar = DistanceSensor(echo=ULTRASONIC_ECHO, trigger=ULTRASONIC_TRIG)
    return robot, sonar


# ─── DETECTION ─────────────────────────────────────────────────────

def detect_person(frame, interpreter, input_details, output_details):
    """
    Run TFLite inference on a frame.
    Returns the largest person bounding box as (x, y, w, h) in pixels,
    or None if no person detected.
    """
    # Preprocess
    img = np.resize(frame, (1, INPUT_SIZE[0], INPUT_SIZE[1], 3)).astype(np.uint8)
    interpreter.set_tensor(input_details[0]["index"], img)
    interpreter.invoke()

    # Parse outputs
    boxes = interpreter.get_tensor(output_details[0]["index"])[0]    # [N, 4]
    classes = interpreter.get_tensor(output_details[1]["index"])[0]  # [N]
    scores = interpreter.get_tensor(output_details[2]["index"])[0]   # [N]

    best_box = None
    best_area = 0

    for i in range(len(scores)):
        if int(classes[i]) == PERSON_CLASS_ID and scores[i] >= CONFIDENCE_THRESHOLD:
            ymin, xmin, ymax, xmax = boxes[i]
            x = int(xmin * FRAME_WIDTH)
            y = int(ymin * FRAME_HEIGHT)
            w = int((xmax - xmin) * FRAME_WIDTH)
            h = int((ymax - ymin) * FRAME_HEIGHT)
            area = w * h
            if area > best_area:
                best_area = area
                best_box = (x, y, w, h)

    return best_box


# ─── STEERING ──────────────────────────────────────────────────────

def compute_steering(bbox):
    """
    Given a person bounding box (x, y, w, h), compute left/right motor speeds.
    Returns (left_speed, right_speed) each in range [-1, 1].
    """
    x, y, w, h = bbox
    person_center_x = x + w / 2
    frame_center_x = FRAME_WIDTH / 2

    # Horizontal error: negative = person is left, positive = person is right
    error = (person_center_x - frame_center_x) / FRAME_WIDTH  # -0.5 to +0.5

    # Distance control: bbox area vs target
    area_ratio = (w * h) / (FRAME_WIDTH * FRAME_HEIGHT)
    if area_ratio > TARGET_AREA_RATIO + AREA_TOLERANCE:
        # Too close — slow down or stop
        speed = 0.0
    elif area_ratio < TARGET_AREA_RATIO - AREA_TOLERANCE:
        # Too far — drive forward
        speed = BASE_SPEED
    else:
        # In the sweet spot — creep
        speed = BASE_SPEED * 0.3

    left_speed = speed + (error * KP)
    right_speed = speed - (error * KP)

    # Clamp
    left_speed = max(-1.0, min(1.0, left_speed))
    right_speed = max(-1.0, min(1.0, right_speed))

    return left_speed, right_speed


def drive(robot, left_speed, right_speed):
    """Send speed commands to motors."""
    if left_speed >= 0 and right_speed >= 0:
        robot.value = (left_speed, right_speed)
    elif left_speed < 0 and right_speed >= 0:
        robot.value = (left_speed, right_speed)  # gpiozero handles negative = reverse
    elif left_speed >= 0 and right_speed < 0:
        robot.value = (left_speed, right_speed)
    else:
        robot.value = (left_speed, right_speed)


# ─── MAIN LOOP ─────────────────────────────────────────────────────

def main():
    print("[FloorCrew] Initializing escort bot...")
    camera = init_camera()
    interpreter, input_det, output_det = init_tflite(MODEL_PATH)
    robot, sonar = init_robot()
    last_seen = time.time()

    print("[FloorCrew] Ready. Looking for person to follow...")

    try:
        while True:
            frame = camera.capture_array()

            # Obstacle override
            if sonar.distance < STOP_DISTANCE:
                robot.stop()
                print(f"[STOP] Obstacle at {sonar.distance:.2f}m")
                time.sleep(0.1)
                continue

            # Detect person
            bbox = detect_person(frame, interpreter, input_det, output_det)

            if bbox is not None:
                last_seen = time.time()
                left, right = compute_steering(bbox)
                drive(robot, left, right)
                x, y, w, h = bbox
                print(f"[FOLLOW] person@({x},{y}) size={w}x{h} → L={left:.2f} R={right:.2f}")
            else:
                # No person detected
                elapsed = time.time() - last_seen
                if elapsed > LOST_TIMEOUT:
                    robot.stop()
                    print(f"[WAIT] No person for {elapsed:.1f}s — stopped")
                else:
                    print(f"[SEARCH] Lost person, waiting {LOST_TIMEOUT - elapsed:.1f}s...")

            time.sleep(0.05)  # ~20 FPS cap

    except KeyboardInterrupt:
        print("\n[FloorCrew] Shutting down.")
    finally:
        robot.stop()
        camera.stop()


if __name__ == "__main__":
    main()
