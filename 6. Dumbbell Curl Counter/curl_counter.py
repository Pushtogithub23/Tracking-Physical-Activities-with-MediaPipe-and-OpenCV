import mediapipe as mp
import cv2 as cv
from utils import draw_text_with_bg
from Pose_estimationModule import PoseDetector

# Initializing the pose detector and video capture
detector = PoseDetector()
cap = cv.VideoCapture("VIDEOS/INPUTS/dumbbell_curl_single_hand.mp4")
w, h, fps = (int(cap.get(x)) for x in (cv.CAP_PROP_FRAME_WIDTH, cv.CAP_PROP_FRAME_HEIGHT, cv.CAP_PROP_FPS))
filename = "VIDEOS/OUTPUTS/dumbbell_curl_counter.mp4"
out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Checking if video is opened successfully
if not cap.isOpened():
    print("Error: couldn't open the video!")

# Initializing counting and state variables
count = 0
in_up_position = False  # Tracking whether the arm is in the up position
in_down_position = True  # Tracking whether the arm is in the down position initially
color = (0, 0, 255)  # Starting with red color for the 'down' position


# Function to detect the position of the wrist relative to the elbow
def detect_arm_position(landmarks, in_up_position, in_down_position, count, color):
    """
    Detecting the position of the arm (up or down) based on wrist and elbow landmarks.
    Updating the count and color accordingly.

    Args:
        landmarks: Detected landmarks of the pose.
        in_up_position: Boolean indicating whether the arm is in the up position.
        in_down_position: Boolean indicating whether the arm is in the down position.
        count: Current count of repetitions.
        color: Current color representing the arm's position.

    Returns:
        in_up_position: Updated boolean for the up position.
        in_down_position: Updated boolean for the down position.
        count: Updated count based on position changes.
        color: Updated color depending on arm position.
    """
    right_elbow = landmarks[14]
    right_wrist = landmarks[16]

    # Checking if the wrist is above the elbow (up position)
    if right_wrist[1] < right_elbow[1] and not in_up_position and in_down_position:
        count += 1
        in_up_position = True  # Marking the arm as being in the up position
        in_down_position = False  # Arm is no longer in the down position
        color = (0, 255, 0)  # Green color for up position

    # Checking if the wrist is below the elbow (down position)
    elif right_wrist[1] > right_elbow[1]:
        in_up_position = False  # Arm is no longer in the up position
        in_down_position = True  # Marking the arm as being in the down position
        color = (0, 0, 255)  # Red color for down position

    return in_up_position, in_down_position, count, color


# Main loop for processing video frames
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detecting the pose and extracting landmarks
    frame = detector.find_pose(frame, draw=False)
    landmarks = detector.get_positions(frame)

    # Detecting arm position and updating count and color
    in_up_position, in_down_position, count, color = detect_arm_position(landmarks, in_up_position, in_down_position,
                                                                         count, color)

    # Displaying the count on the frame
    draw_text_with_bg(frame, f"Count: {count}", (0, 50), font_scale=1.5, thickness=3, bg_color=color)

    # Writing the frame to the output video
    out.write(frame)

    # Resizing frame for displaying the video
    resized_frame = cv.resize(frame, (int(0.45 * frame.shape[1]), int(0.45 * frame.shape[0])))
    cv.imshow("Video", resized_frame)

    # Breaking the loop when 'p' key is pressed
    if cv.waitKey(1) & 0xff == ord('p'):
        break

# Releasing video resources and closing display windows
cap.release()
out.release()
cv.destroyAllWindows()
