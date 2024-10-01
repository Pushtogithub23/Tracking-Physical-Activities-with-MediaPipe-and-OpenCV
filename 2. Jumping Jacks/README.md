# Jumping Jacks Counter using MediaPipe's Pose Estimation

This project implements a jumping jacks counter using the MediaPipe pose estimation module integrated with OpenCV. The script detects body landmarks, calculates the angles between key joints (shoulder, hip, elbow), and counts repetitions of the jumping jacks based on arm movements.

![jumping_jacks_count (1)](https://github.com/user-attachments/assets/105a2971-6171-408a-a951-8b2b70cfe2bf)

## Features

- **Pose Estimation**: Uses MediaPipe Pose to detect body landmarks and estimate body pose in real-time.
- **Repetition Counting**: Calculates the angle formed by key joints to determine when the arms are in the "up" or "down" position and counts a repetition when the arms go from "down" to "up".
- **Dynamic Visualization**: Displays the count of repetitions and the current angle of the arms on the video in real-time.
- **Video Processing**: The input video is processed, annotated, and saved as a new output file showing the count and angle calculations.

## Dependencies

The project relies on the following libraries:

- [OpenCV](https://opencv.org/): For reading and writing video files, drawing on the frames, and displaying the output.
- [NumPy](https://numpy.org/): For efficient mathematical operations, particularly for calculating angles.
- [MediaPipe](https://google.github.io/mediapipe/): For pose detection and extracting body landmarks.

Install the necessary dependencies via pip:

```bash
pip install opencv-python numpy mediapipe
```

## Code Overview

### Pose Detection Module

The code uses a `PoseDetector` class from the `Pose_estimationModule` which utilizes MediaPipe's pose estimation to detect the body landmarks and extract key points such as shoulders, hips, and elbows.

```python
detector = PoseDetector()
```

### Step Counting Logic

The script identifies when the arms are in the "up" or "down" position by calculating the angle between the shoulder, elbow, and hip. When the arms are in the "down" position (angle < 50 degrees) and then transition to the "up" position (angle > 100 degrees), the script counts a repetition.

### Video Processing

The script processes an input video, performs pose detection on each frame, and overlays the following on the video:
- The current repetition count.
- The angle formed by the elbow joint.
- A color indicator showing the current arm position: green for "up", red for "down".

### Usage

1. **Input Video**: Place your input video in the `VIDEOS/INPUTS/` directory.
2. **Running the Script**: Run the script to process the input video and generate an annotated output.

```bash
python jumping_jacks_counter.py
```

3. **Output**: The processed video with the annotated count and angles will be saved in the `VIDEOS/OUTPUTS/` directory.

### Functions

- **`calculate_angle(a, b, c)`**: Computes the angle between three landmarks (a, b, c) representing joints.
- **`update_count_and_color_by_angle(angle, stage, count)`**: Updates the repetition count and changes the color based on the arm's position.
- **`draw_text_with_bg(frame, text, position, font_scale, thickness, bg_color)`**: Utility function for drawing text with a background on the frame.

### Example Usage

```python
python jumping_jacks_counter.py
```

This will process the input video (`jumping_jacks.mp4`) and save the result with the jump counts as `jumping_jacks_count.mp4` in the `VIDEOS/OUTPUTS/` directory.

### Future Improvements

- Add functionality to track multiple individuals in a video performing jumping jacks simultaneously.
- Enhance the counter's accuracy by incorporating more body joints (e.g., knees) into the angle calculation logic.

### References
1. [MediaPipe's article on Pose Landmarks Detection](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)
2. [Video by Ketut Subiyanto from Pexels](https://www.pexels.com/video/woman-working-out-on-the-outdoors-5034331/)
---
