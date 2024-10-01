
# Crunches Counter

This project utilizes OpenCV and MediaPipe to count crunches performed in a video. The program processes video input, detects body landmarks, and calculates angles to determine the count of crunches. It visualizes the exercise count and angles on the video feed and saves the output to a new video file.

![crunches_counter](https://github.com/user-attachments/assets/8195bd7e-4ea7-4443-8924-a9780856f3ee)


## Features

- Pose detection and angle calculation using MediaPipe.
- Counts the number of crunches based on body landmark positions.
- Visual feedback with angle readings and count display.
- Outputs the processed video with annotations for further analysis.

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
 ┃ ┗ crunches.mp4              # Input video for processing
 ┣ 📂 OUTPUTS
 ┃ ┗ crunches_counter.mp4      # Output video with crunches counter and angles
📜 Pose_estimationModule.py   # Pose detection module (PoseDetector class)
📜 utils.py                   # Utility functions for text drawing
📜 main.py                    # Main script for crunches counting
```

## How to Use

1. **Input Video**: Place your input video file (e.g., `crunches.mp4`) in the `VIDEOS/INPUTS` directory.
2. **Run the Script**: Execute the `main.py` script to start the counting process:

   ```bash
   python main.py
   ```

3. **View Output**: The output video (`crunches_counter.mp4`) will be saved in the `VIDEOS/OUTPUTS` directory.

4. **Pause the Video**: While the video is playing, you can pause it by pressing the 'p' key.

## Code Overview

### Key Functions

- `calculate_angle(a, b, c)`: Calculates the angle formed by three points.
- `update_count_and_color_by_angle(angle, stage, count)`: Updates the count of crunches and the display color based on the calculated angle and current stage (up/down).

### Pose Detection

The pose estimation is handled by the `PoseDetector` class, which wraps around the MediaPipe Pose Estimation module. This class detects body landmarks in each frame and allows for real-time angle calculations based on joint positions.
![image](https://github.com/user-attachments/assets/857fdead-135e-4d0c-96e8-6c224e851246)


## Customization

You can customize the following parameters in the `main.py` file:

- **Input Video**: Change the input video file path in the `cv.VideoCapture` method.
- **Angle Thresholds**: Modify the angle thresholds in the `update_count_and_color_by_angle` function to suit different exercise styles.

## References
1. [MediaPipe's article on Pose Landmarks Detection](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)
   

---
