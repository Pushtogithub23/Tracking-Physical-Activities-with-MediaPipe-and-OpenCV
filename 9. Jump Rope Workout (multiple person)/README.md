
# Rope Jump Workout Tracker with YOLOv8 and OpenCV

This project is a **Rope Jump Workout Tracker** that uses a **YOLOv8 model** for object detection and tracking of people, along with counting their rope jumps in a video. The program calculates and displays the number of jumps for each tracked individual in real-time.

![rope_jump_workout](https://github.com/user-attachments/assets/c96983d7-5c6b-4a63-8ef6-5d579a0a6667)


## Table of Contents

1. [Features](#features)
2. [How It Works](#how-it-works)
3. [Directory Structure](#directory-structure)
4. [Requirements](#requirements)
5. [Usage](#usage)
6. [Code Overview](#code-overview)
7. [Helper Function (`draw_text_with_bg`)](#helper-function-draw_text_with_bg)
8. [Output Example](#output-example)
9. [References](#references)

## Features

- **Real-Time Detection**: Detects and tracks multiple people using YOLOv8 model weights.
- **Jump Counting**: Counts the number of jumps based on the detected bounding box’s vertical movements.
- **Customizable Parameters**: Jump thresholds can be adjusted for each individual, allowing for flexibility in counting based on jump height.
- **Time Display**: A running timer shows the elapsed time in the video, providing an additional workout metric.
- **Output Video**: The processed video with overlays is saved to a file.

## How It Works

1. **Object Detection**: The script uses YOLOv8n, a lightweight object detection model, to detect people in each video frame.
2. **Tracking**: Each person is assigned a unique ID, allowing their movements to be tracked across frames.
3. **Jump Detection**: Jumps are detected based on the vertical center of the person’s bounding box. If the center rises above a certain threshold (indicating a jump), the jump count increases.
4. **Overlays**: The current jump count and a timer are displayed on the video for each detected person.

## Directory Structure

```
|-- utils.py
|-- rope_jump_workout_tracker.py
|-- VIDEOS/
    |-- INPUTS/
        |-- rope_jumping_2.mp4  # Sample input video
    |-- OUTPUTS/
        |-- rope_jump_workout.mp4  # Processed video output
|-- YOLO_WEIGHTS/
    |-- yolov8n.pt  # YOLOv8n model weights
```

### `utils.py`

The `utils.py` script contains helper functions. The function used in this project is `draw_text_with_bg`, which helps draw text with a rectangular background for better visibility on the video frames using OpenCV.

## Requirements

1. **YOLOv8**: Install the ultralytics package for YOLOv8.
   ```bash
   pip install ultralytics
   ```

2. **OpenCV**: Required for video capture, frame processing, and video writing.
   ```bash
   pip install opencv-python
   ```

3. **NumPy**: For numerical operations in OpenCV.
   ```bash
   pip install numpy
   ```

## Usage

1. **Set up the environment**: Ensure that you have installed the necessary libraries (`ultralytics`, `opencv-python`, `numpy`).

2. **Download YOLOv8n Weights**: Download the YOLOv8n weights and place them in the `YOLO_WEIGHTS` directory. You can download the YOLOv8 weights from the [Ultralytics YOLOv8 repository](https://github.com/ultralytics/ultralytics/blob/main/docs/en/models/yolov8.md)

3. **Run the Script**: Execute the `rope_jump_workout_tracker.py` file to process the input video and generate the output with jump counts.
   ```bash
   python rope_jump_workout_tracker.py
   ```

4. **Output**: The output video will be saved to `VIDEOS/OUTPUTS/rope_jump_workout.mp4` with the jump counts and timer overlayed on the video.

## Code Overview

### 1. Initialize YOLO Model and Video Capture
```python
model = YOLO("YOLO_WEIGHTS/yolov8n.pt")
cap = cv.VideoCapture("VIDEOS/INPUTS/rope_jumping_2.mp4")
```

### 2. Track and Count Jumps
- Each detected person is tracked across frames using the unique `track_id`.
- The center of each person’s bounding box is calculated, and the jump count is updated based on the bounding box's vertical movement.

```python
center_y = (bbox[1] + bbox[3]) // 2  # Calculate bounding box center
process_person(track_id, bbox, center_y)  # Update jump count and status
```

### 3. Draw Overlays
- Draw the number of jumps for each tracked person on the video frame.
- A running timer is displayed at the top-left of the frame indicating the elapsed time.

```python
draw_text_with_bg(frame, f"ID: {track_id}, Jumps: {jump_data[track_id]['count']}",
                  (bbox[0] - 100, center_y), font_scale=0.8, thickness=2, bg_color=colors[track_id],
                  text_color=(0, 0, 0))
draw_timer(frame, current_frame, fps)  # Draw the elapsed time on the frame
```

## Helper Function (`draw_text_with_bg`)

The `draw_text_with_bg` function is a utility function used to draw text with a background rectangle, which improves the visibility of the text overlay.

### Function Definition:

```python
def draw_text_with_bg(frame, text, pos, font=cv.FONT_HERSHEY_SIMPLEX, font_scale=0.3, thickness=1, bg_color=(255, 255, 255),
                      text_color=(0, 0, 0)):
    """Draws text with a background rectangle."""
    (text_width, text_height), baseline = cv.getTextSize(text, font, font_scale, thickness)
    x, y = pos
    cv.rectangle(frame, (x, y - text_height - baseline), (x + text_width, y + baseline), bg_color, cv.FILLED)
    cv.putText(frame, text, (x, y), font, font_scale, text_color, thickness, lineType=cv.LINE_AA)
```

### Function Parameters:

- **frame**: The frame (image) where the text needs to be drawn.
- **text**: The string to be drawn on the frame.
- **pos**: A tuple (x, y) specifying the position of the text.
- **font**: Font type (default is `cv.FONT_HERSHEY_SIMPLEX`).
- **font_scale**: Scale of the font size.
- **thickness**: Thickness of the text.
- **bg_color**: Background color of the rectangle (default is white: `(255, 255, 255)`).
- **text_color**: Color of the text (default is black: `(0, 0, 0)`).

### Usage Example:

```python
draw_text_with_bg(frame, "Jump Count: 5", (10, 50), font_scale=0.5, bg_color=(0, 0, 255), text_color=(255, 255, 255))
```

This function draws a filled rectangle behind the text for better visibility.

## Output Example

The output video contains the following:
- A bounding box around each detected person.
- Jump counts are displayed near the bounding box for each person.
- A timer at the top-left corner indicates the elapsed time.

![rope_jump_workout](https://github.com/user-attachments/assets/d9b3add3-0209-43fb-bfd4-e580ffcd6fec)


## References

- [YOLOv8 Documentation on Multi-Object Tracking](https://docs.ultralytics.com/modes/track/)
- [OpenCV Documentation](https://docs.opencv.org/4.x/d6/d6e/group__imgproc__draw.html)
- [Ultralytics GitHub Repository](https://github.com/ultralytics/ultralytics/blob/main/docs/en/models/yolov8.md)


---
