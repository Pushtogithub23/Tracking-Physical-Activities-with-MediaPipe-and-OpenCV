import cv2 as cv
from utils import draw_text_with_bg
from Pose_estimationModule import PoseDetector

# Initializing the pose detector
detector = PoseDetector()
cap = cv.VideoCapture("VIDEOS/INPUTS/bench_press.mp4")
w, h, fps = (int(cap.get(x)) for x in (cv.CAP_PROP_FRAME_WIDTH, cv.CAP_PROP_FRAME_HEIGHT, cv.CAP_PROP_FPS))
filename = "VIDEOS/OUTPUTS/bench_press_counter.mp4"
out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

if not cap.isOpened():
    print("Error: couldn't open the video!")

# Initializing count and state variables
count = 0
stage = None
color = (0, 0, 255)  # Red for 'down' state

# Function to check and update the state based on the elbow position
def update_count_and_color(elbow, shoulder, stage, count):
    """
    Updating the count and color based on the elbow and shoulder positions.

    Args:
        elbow: Coordinates of the elbow [x, y].
        shoulder: Coordinates of the shoulder [x, y].
        stage: Current stage ('up' or 'down').
        count: Current count of repetitions.

    Returns:
        stage: Updated stage.
        count: Updated count.
        color: Updated color (red for 'down', green for 'up').
    """
    if elbow[1] > shoulder[1]:  # Elbow below shoulder (down position)
        stage = 'down'
        color = (0, 0, 255)  # Red color
    elif elbow[1] < shoulder[1] and stage == 'down':  # Elbow above shoulder (up position)
        count += 1
        stage = 'up'
        color = (0, 255, 0)  # Green color

    return stage, count, color

# Processing the video frame by frame
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Detecting pose and getting landmark positions
    frame = detector.find_pose(frame, draw=False)
    landmarks = detector.get_positions(frame)

    left_shoulder, right_shoulder = landmarks[11], landmarks[12]
    left_elbow, right_elbow = landmarks[13], landmarks[14]

    # Updating count and color based on right arm position
    stage, count, color = update_count_and_color(right_elbow, right_shoulder, stage, count)

    # Displaying the count on the frame
    draw_text_with_bg(frame, f"Count: {count}", (0, 60), font_scale=2, thickness=4, bg_color=color,
                      text_color=(0, 0, 0))

    # Resizing the frame for display
    resizing_factor = 0.45
    resized_shape = (int(resizing_factor * frame.shape[1]), int(resizing_factor * frame.shape[0]))
    resized_frame = cv.resize(frame, resized_shape)

    # Writing the frame to the output video
    out.write(frame)

    # Displaying the resized video
    cv.imshow("Video", resized_frame)

    # Breaking on 'p' key press
    if cv.waitKey(1) & 0xff == ord('p'):
        break

# Releasing video resources
cap.release()
out.release()
cv.destroyAllWindows()
