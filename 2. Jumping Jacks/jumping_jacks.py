import cv2 as cv
import numpy as np
from utils import draw_text_with_bg
from Pose_estimationModule import PoseDetector

# Initializing the pose detector
detector = PoseDetector()
cap = cv.VideoCapture("VIDEOS/INPUTS/jumping_jacks.mp4")
w, h, fps = (int(cap.get(x)) for x in (cv.CAP_PROP_FRAME_WIDTH, cv.CAP_PROP_FRAME_HEIGHT, cv.CAP_PROP_FPS))
filename = "VIDEOS/OUTPUTS/jumping_jacks_count.mp4"
out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

if not cap.isOpened():
    print("Error: couldn't open the video!")

# Initializing state variables for both hands
count = 0
stage = None  # 'up' or 'down'
color = (0, 0, 255)  # Red for down, green for up

# Function to calculate the angle formed by three points
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
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    ab = a - b  # Vector from shoulder to elbow
    bc = c - b  # Vector from elbow to wrist

    cosine_angle = np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc))
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)  # Clipping to avoid domain error in arccos
    angle = np.degrees(np.arccos(cosine_angle))

    return angle

# Function for counting and setting color based on angle
def update_count_and_color_by_angle(angle, stage, count):
    """
    Updating the count and color based on the elbow angle.

    Args:
        angle: The current elbow angle in degrees.
        stage: The current stage of the arm ('up' or 'down').
        count: The current count of repetitions.

    Returns:
        stage: Updated stage ('up' or 'down').
        count: Updated repetition count.
        color: Updated color (green for 'up', red for 'down').
    """
    if angle < 50:  # "down" position
        stage = "down"
        color = (0, 0, 255)  # Setting red color for down position
    elif angle > 100 and stage == "down":  # "up" position and counting repetition
        count += 1
        stage = "up"
        color = (0, 255, 0)  # Setting green color for up position
    else:
        # Keeping the current color if no state change
        color = (0, 255, 0) if stage == "up" else (0, 0, 255)

    return stage, count, color

# Main loop for processing video frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detecting pose and getting landmark positions
    frame = detector.find_pose(frame, draw=False)
    landmarks = detector.get_positions(frame)

    # Getting left and right elbow/wrist/shoulder landmarks
    left_shoulder = landmarks[11]
    left_hip = landmarks[23]
    left_elbow = landmarks[13]

    right_shoulder = landmarks[12]
    right_hip = landmarks[24]
    right_elbow = landmarks[14]

    # Calculating the angle for both arms
    angle_left = calculate_angle(left_hip, left_shoulder, left_elbow)
    angle_right = calculate_angle(right_hip, right_shoulder, right_elbow)
    
    # Updating right hand count and color based on angle
    stage, count, color = update_count_and_color_by_angle(angle_left, stage, count)

    # Displaying the count and angle for both hands on the frame
    draw_text_with_bg(frame, f"Count: {count}", (0, 50), font_scale=1.5, thickness=2, bg_color=color)

    # Drawing lines between shoulder, hip, and elbow
    cv.line(frame, left_shoulder, left_hip, (255, 255, 255), 2)
    cv.line(frame, left_shoulder, left_elbow, (255, 255, 255), 2)
    cv.line(frame, right_shoulder, right_hip, (255, 255, 255), 2)
    cv.line(frame, right_shoulder, right_elbow, (255, 255, 255), 2)

    # Displaying the angles on the frame
    draw_text_with_bg(frame, f"{int(angle_left)} degrees", left_shoulder, font_scale=0.8, thickness=2)
    draw_text_with_bg(frame, f"{int(angle_left)} degrees", (right_shoulder[0] - 100, right_shoulder[1]), font_scale=0.8, thickness=2)

    # Writing the frame to the output video
    out.write(frame)

    # Resizing the frame for display
    resizing_factor = 0.45
    resized_shape = (int(resizing_factor * frame.shape[1]), int(resizing_factor * frame.shape[0]))
    resized_frame = cv.resize(frame, resized_shape)

    # Displaying the video
    cv.imshow("Video", resized_frame)

    # Breaking the loop on 'p' key press
    if cv.waitKey(1) & 0xff == ord('p'):
        break

# Releasing video resources
cap.release()
out.release()
cv.destroyAllWindows()
