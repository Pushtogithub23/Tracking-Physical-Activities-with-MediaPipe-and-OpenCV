# Push-Up and Jump Counter with Pose Estimation

This project uses computer vision and pose estimation techniques to count push-ups and jumps performed by a user in a video. The implementation utilizes the MediaPipe library for pose detection, wrapped in a custom `PoseDetector` module. It calculates angles between key body landmarks to determine the current state of the exercise and updates counts accordingly.

## Features

- **Push-Up Counter**: Counts the number of push-ups performed based on the angle between the shoulder, elbow, and wrist.
- **Jump Counter**: Counts the number of jumps based on the vertical position of the wrist relative to the heel.
- **Visual Feedback**: Displays the counts and angles on the video frame for real-time feedback.

## Prerequisites

To run this project, you'll need the following:

- Python 3.7 or higher
- OpenCV
- NumPy
- MediaPipe
- A compatible video file (e.g., MP4 format) for testing

You can install the required Python packages using pip:

```bash
pip install opencv-python numpy mediapipe
```

## Directory Structure

```
.
├── VIDEOS
│   ├── INPUTS
│   │   └── pushups.mp4
│   └── OUTPUTS
│       └── push-ups_counter.mp4
├── utils.py
├── Pose_estimationModule.py
└── pushup_jump_counter.py
```

- `VIDEOS/INPUTS`: Place your input video files here.
- `VIDEOS/OUTPUTS`: The output video with counted exercises will be saved here.
- `utils.py`: Contains utility functions for drawing text on the video frames.
- `Pose_estimationModule.py`: Wraps the MediaPipe pose estimation module to detect and draw body landmarks.
- `pushup_jump_counter.py`: Main script to run the push-up and jump counting application.

## Usage

1. Place your input video file in the `VIDEOS/INPUTS` directory and name it `pushups.mp4`.
2. Run the script:

```bash
python pushup_jump_counter.py
```

3. The processed video will be saved in the `VIDEOS/OUTPUTS` directory as `push-ups_counter.mp4`.
4. The video window will display the push-up and jump counts along with the angles of the right elbow.

## Code Overview

### Key Functions

- `calculate_angle(a, b, c)`: Calculates the angle formed by three points (e.g., shoulder, elbow, wrist).
  
- `update_count_and_color_by_angle(angle, stage, count)`: Updates the count of push-ups based on the elbow angle and changes the color displayed on the screen.

- `detect_jump(heel, wrist, stage, count)`: Detects jumps based on the wrist position relative to the heel and updates the jump count.

### Example of Pose Detection

The pose estimation is performed using the `PoseDetector` class that leverages MediaPipe's pose detection capabilities. It detects key body landmarks, which are then used to calculate angles and states for counting exercises.

## References
1. [MediaPipe's article on Pose Landmarks Detection](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)
2. [Video by RDNE Stock project from Pexels](https://www.pexels.com/video/a-man-doing-push-ups-on-grass-7187079/)

---
