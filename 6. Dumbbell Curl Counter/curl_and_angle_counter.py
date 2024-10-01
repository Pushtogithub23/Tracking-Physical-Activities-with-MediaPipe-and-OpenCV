import cv2 as cv
import numpy as np
from utils import draw_text_with_bg
from Pose_estimationModule import PoseDetector

# Initializing pose detector
detector = PoseDetector()
cap = cv.VideoCapture("VIDEOS/INPUTS/dumbbell_curl.mp4")

# Retrieving video dimensions and frame rate
w, h, fps = (int(cap.get(x)) for x in (cv.CAP_PROP_FRAME_WIDTH, cv.CAP_PROP_FRAME_HEIGHT, cv.CAP_PROP_FPS))
filename = "VIDEOS/OUTPUTS/curl_angle_counter1.mp4"
# Initializing video writer for saving the output video
# out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

if not cap.isOpened():
    print("Error: couldn't open the video!")

# Initializing state variables for both hands
count_right, count_left = 0, 0
stage_right, stage_left = None, None  # Defining 'up' or 'down' stage
color_left, color_right = (0, 0, 255), (0, 0, 255)  # Initializing red color for 'down' position, green for 'up'

# Defining function to calculate the angle formed by three points
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

    ab = a - b  # Defining vector from shoulder to elbow
    bc = c - b  # Defining vector from elbow to wrist

    # Calculating cosine of the angle between the two vectors
    cosine_angle = np.dot(ab, bc) / (np.linalg.norm(ab) * np.linalg.norm(bc))
    cosine_angle = np.clip(cosine_angle, -1.0, 1.0)  # Clipping to avoid domain error in arccos
    angle = np.degrees(np.arccos(cosine_angle))  # Converting the angle to degrees

    return angle

# Predefining function for counting repetitions and setting color based on angle
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
    if angle > 150:  # Checking for "down" position
        stage = "down"
        color = (0, 0, 255)  # Setting red color for down position
    elif angle < 30 and stage == "down":  # Checking for "up" position and increasing count
        count += 1
        stage = "up"
        color = (0, 255, 0)  # Setting green color for up position
    else:
        # Keeping the current color if no state change occurs
        color = (0, 255, 0) if stage == "up" else (0, 0, 255)

    return stage, count, color

# Main loop for reading and processing video frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detecting pose and retrieving landmark positions
    frame = detector.find_pose(frame, draw=False)
    landmarks = detector.get_positions(frame)

    # Getting left and right elbow/wrist/shoulder landmarks
    left_shoulder, right_shoulder = landmarks[11], landmarks[12]
    left_elbow, right_elbow = landmarks[13], landmarks[14]
    left_wrist, right_wrist = landmarks[15], landmarks[16]

    # Calculating the angle for both arms
    angle_right = calculate_angle(right_shoulder, right_elbow, right_wrist)
    angle_left = calculate_angle(left_shoulder, left_elbow, left_wrist)

    # Updating right hand count and color based on the calculated angle
    stage_right, count_right, color_right = update_count_and_color_by_angle(angle_right, stage_right, count_right)

    # Updating left hand count and color based on the calculated angle
    stage_left, count_left, color_left = update_count_and_color_by_angle(angle_left, stage_left, count_left)

    # Displaying the count and angle for both hands on the frame
    draw_text_with_bg(frame, f"Right Hand Count: {count_right}", (0, 50), font_scale=1.25, thickness=2,
                      bg_color=color_right)
    draw_text_with_bg(frame, f"{int(angle_right)} degrees", (right_elbow[0]-75, right_elbow[1]), font_scale=1, thickness=2)

    draw_text_with_bg(frame, f"Left Hand Count: {count_left}", (0, 105), font_scale=1.25, thickness=2,
                      bg_color=color_left)
    draw_text_with_bg(frame, f"{int(angle_left)} degrees", (left_elbow[0]-75, left_elbow[1]), font_scale=1, thickness=2)

    # Writing the frame to the output video
    # out.write(frame)

    # Resizing frame for display
    resizing_factor = 0.45
    resized_shape = (int(resizing_factor * frame.shape[1]), int(resizing_factor * frame.shape[0]))
    resized_frame = cv.resize(frame, resized_shape)

    # Displaying the video
    cv.imshow("Video", resized_frame)

    # Breaking the loop if 'p' is pressed
    if cv.waitKey(1) & 0xff == ord('p'):
        break

# Releasing resources
cap.release()
# out.release()
cv.destroyAllWindows()
