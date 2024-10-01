import cv2 as cv
import numpy as np
from utils import draw_text_with_bg
from Pose_estimationModule import PoseDetector

# Initialize pose detector
detector = PoseDetector()
cap = cv.VideoCapture("VIDEOS/INPUTS/pushups.mp4")
w, h, fps = (int(cap.get(x)) for x in (cv.CAP_PROP_FRAME_WIDTH, cv.CAP_PROP_FRAME_HEIGHT, cv.CAP_PROP_FPS))
filename = "VIDEOS/OUTPUTS/push-ups_counter.mp4"
out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

if not cap.isOpened():
    print("Error: couldn't open the video!")

# Initialize state variables for both hands
count_right = 0
stage_right = None  # 'up' or 'down'
color_right = (0, 0, 255)  # Red for down, green for up
jump_count = 0
jump_stage = None
jump_color = (0, 0, 255)


# Function to calculate the angle formed by three points
def calculate_angle(a, b, c):
    """
    Calculate the angle formed by three points.

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
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)  # Clip to avoid domain error in arccos
    angle = np.degrees(np.arccos(cosine_angle))

    return angle


# Predefined function for counting and setting color based on angle
def update_count_and_color_by_angle(angle, stage, count):
    """
    Update the count and color based on the elbow angle.

    Args:
        angle: The current elbow angle in degrees.
        stage: The current stage of the arm ('up' or 'down').
        count: The current count of repetitions.

    Returns:
        stage: Updated stage ('up' or 'down').
        count: Updated repetition count.
        color: Updated color (green for 'up', red for 'down').
    """
    if angle > 100:  # "down" position
        stage = "up"
        color = (0, 0, 255)  # Red color for down position
    elif angle < 80 and stage == "up":  # "up" position and count
        count += 1
        stage = "down"
        color = (0, 255, 0)  # Green color for up position
    else:
        # Keep the current color if no state change
        color = (0, 255, 0) if stage == "down" else (0, 0, 255)

    return stage, count, color


def detect_jump(heel, wrist, stage, count):
    if wrist[1] >= heel[1]:
        stage = "grounded"
        color = (0, 0, 255)
    elif wrist[1] < heel[1] and stage == 'grounded':
        count += 1
        stage = "jump"
        color = (0, 255, 0)
    else:
        color = (0, 0, 255) if stage == "grounded" else (0, 255, 0)

    return stage, count, color


# Main loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detect pose and get landmark positions
    frame = detector.find_pose(frame, draw=False)
    landmarks = detector.get_positions(frame)

    # Get left and right elbow/wrist/shoulder landmarks
    right_shoulder = landmarks[12]
    right_elbow = landmarks[14]
    right_wrist = landmarks[16]
    right_heel = landmarks[30]

    # Calculate the angle for both arms
    angle_right = calculate_angle(right_shoulder, right_elbow, right_wrist)
    # Update right hand count and color based on angle
    stage_right, count_right, color_right = update_count_and_color_by_angle(angle_right, stage_right, count_right)

    jump_stage, jump_count, jump_color = detect_jump(right_heel, right_wrist, jump_stage, jump_count)

    # Display the count and angle for both hands on the frame
    draw_text_with_bg(frame, f"Push-ups: {count_right}", (0, 50), font_scale=1.25, thickness=2,
                      bg_color=color_right)
    draw_text_with_bg(frame, f"{int(angle_right)} degrees", (right_elbow[0] - 75, right_elbow[1]), font_scale=1,
                      thickness=2)
    draw_text_with_bg(frame, f"Jumps: {jump_count}", (0, 102), font_scale=1.25, thickness=2,
                      bg_color=jump_color)

    # Write the frame to the output video
    out.write(frame)

    # Resize frame for display
    resizing_factor = 0.45
    resized_shape = (int(resizing_factor * frame.shape[1]), int(resizing_factor * frame.shape[0]))
    resized_frame = cv.resize(frame, resized_shape)

    # Display the video
    cv.imshow("Video", resized_frame)

    if cv.waitKey(1) & 0xff == ord('p'):
        break

cap.release()
out.release()
cv.destroyAllWindows()
