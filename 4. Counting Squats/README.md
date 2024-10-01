# Squat Repetition Counter Using MediaPipe's Pose Estimation

This project uses computer vision and pose estimation to track and count squat repetitions in a video. It calculates joint angles, such as the knee and hip angles, to identify the up and down stages of a squat. The program displays the current rep count and joint angles on the video and saves the processed output.

![count_squats](https://github.com/user-attachments/assets/1cf53587-d4c0-4e25-bc47-a53987e7aa14)


## Features

- Detects squats using pose estimation from a video.
- Tracks the user's joint angles to determine the current stage of the squat (up or down).
- Automatically counts the number of squat repetitions.
- Overlays the squat count and joint angles on the video.
- Saves the processed video with visual feedback as an output.

## Dependencies

To run this project, you need to install the following libraries:

- OpenCV: Used for video processing and drawing on frames.
- Numpy: Used for calculating angles between body joints.
- Mediapipe: Used for detecting necessary body landmarks.
- Custom Modules:
  - `Pose_estimationModule`: A custom module for detecting poses and extracting landmarks.
  - `utils`: A custom module for drawing text with a background on the frame.

### Installation

You can install the dependencies using the following:

```bash
pip install opencv-python numpy mediapipe
```

Ensure that the custom modules `Pose_estimationModule.py` and `utils.py` are also available in the project folder.

## How It Works

1. The program reads the input video and uses the pose estimation model to detect key body landmarks (e.g., shoulder, hip, knee, ankle).
2. It calculates the angles formed at the knee and hip joints using these landmarks.
3. The program uses these angles to determine the up and down stages of the squat:
   - **Up position**: When the knee angle is greater than 100°.
   - **Down position**: When the knee angle is less than 90°, which also increments the squat count.
4. The repetition count and the joint angles are displayed on the video in real-time.
5. The output video is saved with the squat counter overlaid on the frames.

## File Structure

```
📂 VIDEOS
 ┣ 📂 INPUTS
 ┃ ┗ squats.mp4              # Input video for processing
 ┣ 📂 OUTPUTS
 ┃ ┗ count_squats.mp4         # Output video with squat counter and angles
📜 Pose_estimationModule.py   # Pose detection module (PoseDetector class)
📜 utils.py                   # Utility functions for text drawing
📜 main.py                    # Main script for squat counting
```

## Usage

1. Place the input video file (`squats.mp4`) in the `VIDEOS/INPUTS/` directory.
2. Run the `main.py` script:

```bash
python main.py
```

3. The program will process the video and save the output as `count_squats.mp4` in the `VIDEOS/OUTPUTS/` folder with the rep count and joint angles overlay.

## Customization

- **Input video**: Modify the path to the input video if you want to analyze a different file.
- **Joint Angle Thresholds**: You can adjust the angle thresholds to identify the up and down stages of the squat in the `update_count_and_color_by_angle()` function.
- **Landmarks**: The current implementation tracks the right side of the body (right shoulder, hip, knee, and ankle). You can extend this to track both sides if needed.

## References
1. [MediaPipe's article on Pose Landmarks Detection](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)
2. [Video by MART  PRODUCTION from Pexels](https://www.pexels.com/video/a-woman-in-activewear-doing-squats-at-home-8837221/)
---
