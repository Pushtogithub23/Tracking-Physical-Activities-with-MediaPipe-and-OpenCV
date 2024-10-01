
# Dumbbell Curl Counter

This project implements a dumbbell curl counter using OpenCV and MediaPipe for pose detection. The code analyzes video input to detect body landmarks, calculates the angles of the arms, and counts the number of repetitions based on the position of the arms. The output is a video annotated with the count of repetitions and angle measurements.

## Features

- Real-time pose detection and angle calculation using MediaPipe.
- Counts the number of dumbbell curls based on arm positions.
- Displays angles for both arms and visual feedback with colors (red for "down" and green for "up").
- Saves the processed video with annotations for further analysis.

## Requirements

- Python 3.x
- OpenCV
- NumPy
- MediaPipe

You can install the required packages using pip:

```bash
pip install opencv-python numpy mediapipe
```

## Directory Structure

```
📂 VIDEOS
 ┣ 📂 INPUTS
 ┃ ┗ dumbbell_curl.mp4        # Input video for processing
 ┣ 📂 OUTPUTS
 ┃ ┗ curl_angle_counter1.mp4   # Output video with curl counter and angles
📜 Pose_estimationModule.py     # Pose detection module (PoseDetector class)
📜 utils.py                     # Utility functions for text drawing
📜 main.py                      # Main script for dumbbell curl counting
```

## How to Use

1. **Input Video**: Place your input video file (e.g., `dumbbell_curl.mp4`) in the `VIDEOS/INPUTS` directory.
2. **Run the Script**: Execute the `main.py` script to start the counting process:

   ```bash
   python main.py
   ```

3. **View Output**: The output video (`curl_angle_counter1.mp4`) will be saved in the `VIDEOS/OUTPUTS` directory.

4. **Pause the Video**: While the video is playing, you can pause it by pressing the 'p' key.

## Code Overview

### Key Functions

- `calculate_angle(a, b, c)`: Calculates the angle formed by three points (e.g., shoulder, elbow, wrist).
- `update_count_and_color_by_angle(angle, stage, count)`: Updates the count of curls and the display color based on the angle and current stage of the arm.

### Pose Detection

The pose estimation is handled by the `PoseDetector` class, which wraps around the MediaPipe Pose Estimation module. This class detects body landmarks in each frame and allows for real-time angle calculations based on joint positions.

## Customization

You can customize the following parameters in the `main.py` file:

- **Input Video**: Change the input video file path in the `cv.VideoCapture` method.
- **Angle Thresholds**: Modify the angle thresholds in the `update_count_and_color_by_angle` function to suit different exercise styles.

## References
1. [MediaPipe's article on Pose Landmarks Detection](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)
2. [Video by ShotPot from Pexels](https://www.pexels.com/video/a-man-performing-dumbbell-set-4117851/)
3. [Video by Tima Miroshnichenko from Pexels](https://www.pexels.com/video/a-man-working-out-using-dumbbell-5319094/)
---
