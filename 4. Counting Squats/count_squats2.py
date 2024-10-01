import cv2 as cv
import numpy as np
from utils import draw_text_with_bg
from Pose_estimationModule import PoseDetector

# Initializing pose detector and video capture
detector = PoseDetector()
cap = cv.VideoCapture("VIDEOS/INPUTS/squats.mp4")

# Getting video properties (width, height, FPS) and setting up the output file for saving
w, h, fps = (int(cap.get(x)) for x in (cv.CAP_PROP_FRAME_WIDTH, cv.CAP_PROP_FRAME_HEIGHT, cv.CAP_PROP_FPS))
filename = "VIDEOS/OUTPUTS/count_squats.mp4"
out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

if not cap.isOpened():
    print("Error: couldn't open the video!")

# Initializing state variables for counting repetitions and detecting stage (up/down)
count = 0
stage = None  # 'up' or 'down'
color = (0, 0, 255)  # Defaulting to red color for the 'down' stage


# Defining a function for calculating the angle formed by three points (e.g., shoulder, elbow, wrist)
def calculate_angle(a, b, c):
    """
    Calculating the angle formed by three points.
    Args:
        a: First point (e.g., shoulder) [x, y].
        b: Middle point (e.g., elbow) [x, y].
        c: Third point (e.g., wrist) [x, y].
    Returns:
        angle: Angle in degrees between the vectors ab and bc.
    """
    a, b, c = np.array(a), np.array(b), np.array(c)
    ab, bc = a - b, c - b  # Creating vectors from point b to a, and point b to c
    cosine_angle = np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc))
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)  # Clipping to prevent domain error in arccos
    return np.degrees(np.arccos(cosine_angle))


# Defining a function for updating the count and stage based on joint angle (e.g., knee angle)
def update_count_and_color_by_angle(angle, stage, count):
    """
    Updating the count and color based on the detected angle.
    Args:
        angle: The current joint angle in degrees.
        stage: The current stage ('up' or 'down').
        count: The current repetition count.
    Returns:
        stage: Updated stage ('up' or 'down').
        count: Updated repetition count.
        color: Updated color (green for 'up', red for 'down').
    """
    if angle > 100:  # 'up' stage
        stage = "up"
        color = (0, 0, 255)  # Setting red for 'up' position
    elif angle < 90 and stage == "up":  # 'down' stage, incrementing count
        count += 1
        stage = "down"
        color = (0, 255, 0)  # Setting green for 'down' position
    else:
        # Maintaining the color based on the current stage
        color = (0, 255, 0) if stage == "down" else (0, 0, 255)
    return stage, count, color


# Main loop for processing the video frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detecting pose and extracting landmarks
    frame = detector.find_pose(frame, draw=False)
    landmarks = detector.get_positions(frame)

    # Extracting right-side landmarks for shoulder, hip, knee, and ankle
    right_shoulder, right_hip = landmarks[12], landmarks[24]
    right_knee, right_ankle = landmarks[26], landmarks[28]

    # Calculating the knee and hip angles
    angle_knee = calculate_angle(right_hip, right_knee, right_ankle)
    angle_hip = calculate_angle(right_shoulder, right_hip, right_knee)

    # Updating squat count and color based on knee angle
    stage, count, color = update_count_and_color_by_angle(angle_knee, stage, count)

    # Displaying squat count and angles on the frame
    draw_text_with_bg(frame, f"Count: {count}", (0, 50), font_scale=1.5, thickness=2, bg_color=color)

    # Drawing lines between joints
    cv.line(frame, right_shoulder, right_hip, (255, 255, 255), 2)
    cv.line(frame, right_hip, right_knee, color, 2)
    cv.line(frame, right_knee, right_ankle, color, 2)

    # Displaying joint angles near corresponding landmarks
    draw_text_with_bg(frame, f"{int(angle_knee)} degrees", right_knee, font_scale=0.8, thickness=2)
    draw_text_with_bg(frame, f"{int(angle_hip)} degrees", (right_hip[0] - 100, right_hip[1]), font_scale=0.8,
                      thickness=2)

    # Saving the processed frame to the output video
    out.write(frame)

    # Resizing frame for displaying
    resizing_factor = 0.45
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
