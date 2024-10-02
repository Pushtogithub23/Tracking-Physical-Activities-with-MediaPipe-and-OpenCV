import cv2 as cv
from ultralytics import YOLO
from utils import draw_text_with_bg

# Initialize YOLO model and video capture
model = YOLO(r"D:\PyCharm\PyCharm_files\OBJECT DETECTION\YOLO_WEIGHTS\yolov8n.pt")  # replace this path with the path where the YOLOv8n model's weight is downloaded
class_names = list(model.names.values())
cap = cv.VideoCapture("VIDEOS/INPUTS/rope_jumping_2.mp4")
w, h, fps = (int(cap.get(x)) for x in (cv.CAP_PROP_FRAME_WIDTH, cv.CAP_PROP_FRAME_HEIGHT, cv.CAP_PROP_FPS))
filename = "VIDEOS/OUTPUTS/rope_jump_workout.mp4"
out = cv.VideoWriter(filename, cv.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Initialize tracking and counting dictionaries
jump_data = {track_id: {"count": 0, "in_jump": False, "rest_center": 0} for track_id in []}
jump_thresholds = {}  # Jump thresholds per person
colors = {}  # Color for each tracked ID
default_threshold = {"low": 30, "high": 100}  # Default jump thresholds

# Helper functions
def detect_jump(center_y, resting_center, low_thres, high_thres):
    """Check if jump is detected based on center y-coordinate and thresholds."""
    return resting_center - high_thres < center_y < resting_center - low_thres

def process_person(track_id, bbox, center_y):
    """Process each person detected, update jump count and color."""
    if track_id not in jump_data:
        jump_data[track_id] = {"count": 0, "in_jump": False, "rest_center": center_y}
        jump_thresholds[track_id] = default_threshold  # Assign thresholds
        colors[track_id] = (0, 255, 0)  # Default color

    # Unpack necessary details
    low_thres, high_thres = jump_thresholds[track_id]["low"], jump_thresholds[track_id]["high"]
    rest_center = jump_data[track_id]["rest_center"]
    jump_detected = detect_jump(center_y, rest_center, low_thres, high_thres)

    # Update jump status
    if jump_detected and not jump_data[track_id]["in_jump"]:
        jump_data[track_id]["in_jump"] = True
        jump_data[track_id]["count"] += 1
        colors[track_id] = (255, 0, 0) if track_id == 1 else (0, 0, 255) if track_id == 2 else (255, 255, 0)
    elif not jump_detected:
        jump_data[track_id]["in_jump"] = False

def draw_timer(frame, current_frame, fps):
    """Draw timer and jump counts on the frame based on frame number and fps."""
    elapsed_time = current_frame / fps  # Elapsed time based on frame number and fps
    time_display = f"{int(elapsed_time // 60)}:{int(elapsed_time % 60):02}"
    draw_text_with_bg(frame, time_display, (5, 50), font_scale=2, thickness=2, bg_color=(255, 255, 255), text_color=(0, 0, 0))

current_frame = 0  # Initialize frame counter

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Run YOLO model and get results
    results = model.track(frame, persist=True)
    if results[0].boxes.id is not None:
        for bbox, track_id, class_id in zip(results[0].boxes.xyxy.int().cpu().tolist(),
                                            results[0].boxes.id.int().cpu().tolist(),
                                            results[0].boxes.cls.int().cpu().tolist()):
            if class_names[class_id] == 'person':
                center_y = (bbox[1] + bbox[3]) // 2  # Calculate bounding box center
                process_person(track_id, bbox, center_y)  # Process person tracking

                # Draw jump count on the frame
                draw_text_with_bg(frame, f"ID: {track_id}, Jumps: {jump_data[track_id]['count']}",
                                  (bbox[0] - 100, center_y), font_scale=0.8, thickness=2, bg_color=colors[track_id],
                                  text_color=(0, 0, 0))

    # Draw time overlay based on frame number and fps
    draw_timer(frame, current_frame, fps)
    out.write(frame)  # Write to output file

    # Display resized frame
    resized_frame = cv.resize(frame, (int(0.75 * frame.shape[1]), int(0.75 * frame.shape[0])))
    cv.imshow("Video", resized_frame)

    # Increment frame count
    current_frame += 1

    # Exit on pressing 'p'
    if cv.waitKey(1) & 0xff == ord('p'):
        break

# Release resources
cap.release()
out.release()
cv.destroyAllWindows()
