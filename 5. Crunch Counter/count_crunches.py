import cv2 as cv
import numpy as np
from utils import draw_text_with_bg
from Pose_estimationModule import PoseDetector

# Initializing pose detector and capturing video
detector = PoseDetector()
cap = cv.VideoCapture("VIDEOS/INPUTS/crunches.mp4")
w, h, fps = (int(cap.get(x)) for x in (cv.CAP_PROP_FRAME_WIDTH, cv.CAP_PROP_FRAME_HEIGHT, cv.CAP_PROP_FPS))
filename = "VIDEOS/OUTPUTS/crunches_counter.mp4"
out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

if not cap.isOpened():
    print("Error: couldn't open the video!")

# Initializing counting and state variables
count_left, stage_left = 0, None  # Tracking count and stage ('up' or 'down')
color = (0, 0, 255)  # Setting initial color to red for 'down' position

# Defining function for calculating the angle formed by three points (e.g., shoulder, elbow, wrist)
def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    ab, bc = a - b, c - b
    cosine_angle = np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc))
    angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))  # Clipping to avoid domain errors
    return angle

# Defining function for updating count and color based on angle and stage
def update_count_and_color_by_angle(angle, stage, count):
    if angle > 60:  # Checking for 'down' position
        stage, color = "down", (0, 0, 255)  # Setting color to red for 'down'
    elif angle < 50 and stage == "down":  # Transitioning to 'up' and incrementing count
        count, stage, color = count + 1, "up", (0, 255, 0)  # Setting color to green for 'up'
    else:
        color = (0, 255, 0) if stage == "up" else (0, 0, 255)  # Keeping current color
    return stage, count, color

# Processing video frames in a loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detecting pose and getting landmarks
    frame = detector.find_pose(frame, draw=False)
    landmarks = detector.get_positions(frame)

    # Retrieving relevant landmarks for the left side (shoulder, hip, knee)
    left_shoulder, left_hip, left_knee = landmarks[11], landmarks[23], landmarks[25]

    # Calculating the angle for the left side and updating count, stage, and color
    angle_left = calculate_angle(left_knee, left_hip, left_shoulder)
    stage_left, count_left, color = update_count_and_color_by_angle(angle_left, stage_left, count_left)

    # Displaying count and angle on the frame
    draw_text_with_bg(frame, f"Count: {count_left}", (0, 50), font_scale=1.5, thickness=2, bg_color=color)
    cv.line(frame, left_shoulder, left_hip, (255, 255, 255), 2)
    cv.line(frame, left_hip, left_knee, (255, 255, 255), 2)
    draw_text_with_bg(frame, f"{int(angle_left)} degrees", left_hip, font_scale=1, thickness=2)

    # Saving the video
    out.write(frame)

    # Resizing frame for displaying and showing the video
    resized_frame = cv.resize(frame, (int(0.45 * frame.shape[1]), int(0.45 * frame.shape[0])))
    cv.imshow("Video", resized_frame)

    if cv.waitKey(30) & 0xff == ord('p'):  # Pausing video if 'p' is pressed
        break

# Releasing video capture and closing all windows
cap.release()
out.release()
cv.destroyAllWindows()
