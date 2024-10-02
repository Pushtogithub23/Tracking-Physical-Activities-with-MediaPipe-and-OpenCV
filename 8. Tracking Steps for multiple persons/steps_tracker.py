import cv2 as cv
from ultralytics import YOLO
from PoseEstimationModule import PoseDetector
from utils import draw_text_with_bg

# Initializing YOLO model for object detection
model = YOLO(r"D:\PyCharm\PyCharm_files\OBJECT DETECTION\YOLO_WEIGHTS\yolov8n.pt")
class_names = list(model.names.values())  # List of class names from the YOLO model

# Initializing pose detector and video capture
detector = PoseDetector()
cap = cv.VideoCapture("VIDEOS/INPUTS/people_jogging.mp4")

# Getting video properties (width, height, FPS) for proper output file settings
w, h, fps = (int(cap.get(x)) for x in (cv.CAP_PROP_FRAME_WIDTH, cv.CAP_PROP_FRAME_HEIGHT, cv.CAP_PROP_FPS))
filename = "VIDEOS/OUTPUTS/steps_counter.mp4"
out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Ensures video capture opens successfully
if not cap.isOpened():
    print("Error: Couldn't open the video!")

# Initializing step count and movement stage for each person
step_count = {}
movement_stage = {}


# Function to detect and count steps based on ankle movements
def detect_and_count_steps(right_ankle, left_ankle, stage, count):
    """
    Detect and count steps based on the position of ankles.

    Args:
        right_ankle: Coordinates (x, y) of the right ankle.
        left_ankle: Coordinates (x, y) of the left ankle.
        stage: Current step stage ('right_up' or 'left_up').
        count: Current step count.

    Returns:
        Updated stage and step count.
    """
    if right_ankle[1] < left_ankle[1] and stage != 'right_up':  # Right ankle goes above left
        stage = 'right_up'
        count += 1
    elif left_ankle[1] < right_ankle[1] and stage != 'left_up':  # Left ankle goes above right
        stage = 'left_up'
        count += 1
    return stage, count


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO model detects and tracks people in the current frame
    results = model.track(frame, persist=True)
    if results[0].boxes.id is not None:
        bboxes = results[0].boxes.xyxy.int().cpu().tolist()
        track_ids = results[0].boxes.id.int().cpu().tolist()
        class_ids = results[0].boxes.cls.int().cpu().tolist()

        # Looping through detected people in the frame
        for bbox, track_id, class_id in zip(bboxes, track_ids, class_ids):
            x1, y1, x2, y2 = bbox
            class_name = class_names[class_id]

            # Processing only 'person' detections
            if class_name == 'person':
                # Extracting the region of interest (ROI) for pose detection
                ROI = frame[y1:y2, x1:x2]
                ROI = detector.find_pose(ROI, draw=False)
                landmarks = detector.get_positions(ROI)

                # Ensure both ankle landmarks (left and right) are detected
                if 27 in landmarks and 28 in landmarks:
                    left_ankle = landmarks[27]
                    right_ankle = landmarks[28]

                    # Initializing step count and stage for new track IDs
                    if track_id not in step_count:
                        step_count[track_id] = 0
                        movement_stage[track_id] = None

                    # Updating movement stage and step count for the current person
                    movement_stage[track_id], step_count[track_id] = detect_and_count_steps(
                        right_ankle, left_ankle, movement_stage[track_id], step_count[track_id]
                    )

                    # Displaying track ID and step count on the frame
                    draw_text_with_bg(frame, f"ID: {track_id}, Steps: {step_count[track_id]}", (x1, y1-20),
                                      font_scale=0.8, thickness=2)

    # writing the frames for saving the video
    out.write(frame)
    # Resizing frame for better display (optional)
    resizing_factor = 0.45
    resized_shape = (int(resizing_factor * frame.shape[1]), int(resizing_factor * frame.shape[0]))
    resized_frame = cv.resize(frame, resized_shape)

    # Showing the video frame with annotations
    cv.imshow("Video", resized_frame)

    # Exiting the loop if 'p' is pressed
    if cv.waitKey(1) & 0xFF == ord('p'):
        break

# Releasing resources
cap.release()
out.release()
cv.destroyAllWindows()
