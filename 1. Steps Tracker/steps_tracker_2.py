import cv2 as cv
import numpy as np
from utils import draw_text_with_bg
from Pose_estimationModule import PoseDetector

# Initializing pose detector and video capture
detector = PoseDetector()
cap = cv.VideoCapture("VIDEOS/INPUTS/running_2.mp4")

# Getting video properties (width, height, FPS) and setting up the output file for saving
w, h, fps = (int(cap.get(x)) for x in (cv.CAP_PROP_FRAME_WIDTH, cv.CAP_PROP_FRAME_HEIGHT, cv.CAP_PROP_FPS))
filename = "VIDEOS/OUTPUTS/steps_tracker.mp4"
out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

if not cap.isOpened():
    print("Error: couldn't open the video!")

# Initializing state variables for counting steps and detecting stage (up/down)
count = 0
stage = None  # Can be 'right_up' or 'left_up'
color = (0, 0, 255)  # Defaulting to red color for visualization

def detect_and_count_steps(right_ankle, left_ankle, stage, count):
    """
    Detecting and counting steps based on ankle movements.
    Args:
        right_ankle: Coordinates of the right ankle (x, y).
        left_ankle: Coordinates of the left ankle (x, y).
        stage: Current movement stage ('right_up' or 'left_up').
        count: Current step count.
    Returns:
        Updated stage and count.
    """
    if right_ankle[1] < left_ankle[1] and stage != 'right_up':  # Right ankle goes above left
        stage = 'right_up'
        count += 1  # Counting the step
    elif left_ankle[1] < right_ankle[1] and stage != 'left_up':  # Left ankle goes above right
        stage = 'left_up'
        count += 1  # Counting the step

    return stage, count

# Main loop for processing the video frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detecting pose and extracting landmarks
    frame = detector.find_pose(frame, draw = False)
    landmarks = detector.get_positions(frame)
    if 27 in landmarks and 28 in landmarks:
        right_ankle = landmarks[28]  # Assuming landmark 28 is the right ankle
        left_ankle = landmarks[27]   # Assuming landmark 27 is the left ankle

        # Detecting and counting steps based on ankle movements
        stage, count = detect_and_count_steps(right_ankle, left_ankle, stage, count)

        # Displaying the step count on the frame
        draw_text_with_bg(frame, f"Steps: {count}", (0, 40), font_scale=1, thickness=2)

    # Saving the processed frame to the output video
    out.write(frame)

    # Resizing frame for displaying
    resizing_factor = 1
    resized_shape = (int(resizing_factor * frame.shape[1]), int(resizing_factor * frame.shape[0]))
    resized_frame = cv.resize(frame, resized_shape)

    # Displaying the current frame
    cv.imshow("Video", resized_frame)

    # Exiting if the user presses 'p'
    if cv.waitKey(1) & 0xff == ord('p'):
        break

# Releasing video capture and writer, closing display windows
cap.release()
out.release()
cv.destroyAllWindows()
