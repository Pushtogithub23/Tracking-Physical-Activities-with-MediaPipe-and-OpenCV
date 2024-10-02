
# Steps Counter with YOLO and Pose Estimation

This project demonstrates the integration of YOLO object detection with MediaPipe Pose Estimation to count the number of steps taken by people in a video. The code detects human subjects using YOLOv8, applies pose estimation to track their movements, and counts steps based on the movement of ankle landmarks.

![steps_counter](https://github.com/user-attachments/assets/1a26c027-00a0-46a7-8614-d0e27b0a494b)


## Table of Contents
- [Overview](#overview)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Output](#output)
- [Project Structure](#project-structure)
- [References](#References)
## Overview

This project leverages:
- **YOLOv8**: To detect and track people in video frames.
- **MediaPipe's Pose Estimation**: To track body landmarks, specifically focusing on ankle movements to count steps.
- **OpenCV**: For video processing and rendering, the step count is on video frames.

The final output is a video with each detected person's track ID and step count displayed on the screen.

## Requirements

- Python 3.x
- OpenCV
- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) for YOLOv8
- [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide) for Pose Estimation

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Pushtogithub23/Tracking-Physical-Activities-with-MediaPipe-and-OpenCV.git
   cd Tracking-Physical-Activities-with-MediaPipe-and-OpenCV
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download YOLOv8 weights from [Ultralytics](https://huggingface.co/Ultralytics/YOLOv8/blob/main/yolov8n.pt), and place the file in your directory:
   ```plaintext
   yolov8n.pt
   ```


## Usage

1. Place your input video in the `VIDEOS/INPUTS/` folder.

2. Update the script to reference your YOLOv8 weights and the input video.

3. Run the code:
   ```bash
   python steps_tracker.py
   ```

The output video will be saved in `VIDEOS/OUTPUTS/steps_counter.mp4`.

## How It Works

### YOLO Object Detection

The YOLOv8 model is used to detect and track objects in the video, specifically focusing on detecting `person` class instances. The bounding box for each person is used as the region of interest (ROI) for pose detection.

### Pose Estimation

MediaPipe's Pose Estimation is applied to each person's ROI to detect body landmarks. The positions of the left and right ankles (landmarks 27 and 28) are used to detect steps. A step is counted when one ankle moves above the other, simulating the stepping motion.

### Step Counting Logic

The step-counting logic is simple:
- If the right ankle moves above the left, we increment the step count and change the movement stage to `'right_up'`.
- If the left ankle moves above the right, we increment the step count and change the movement stage to `'left_up'`.

Each detected person is assigned a unique track ID, and their steps are tracked separately.

## Output

The output is a video file with each person's:
- **Track ID**: Identifies the individual being tracked.
- **Step Count**: The total number of steps counted for that individual.

The video is annotated with the track ID and the corresponding step count for each detected person.

## Project Structure

```plaintext
📂 steps-counter-yolo
 ┣ 📂 VIDEOS
 ┃ ┣ 📂 INPUTS
 ┃ ┃ ┗ 📄 people_jogging.mp4  # Input video file
 ┃ ┣ 📂 OUTPUTS
 ┃ ┃ ┗ 📄 steps_counter.mp4   # Output video file
 ┣ 📄 utils.py                # Utility function to draw text with background on video
 ┣ 📄 PoseEstimationModule.py # MediaPipe pose detection module
 ┣ 📄 steps_counter.py        # Main script for step counting
 ┣ 📄 requirements.txt        # Dependencies
 ┗ 📄 README.md               # Project documentation
```
## References
1. [MediaPipe's article on Pose Landmark Detection](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)
2. [Ultralytic's guide on Multi-Object Tracking](https://docs.ultralytics.com/modes/track/)
3. [Video by MART  PRODUCTION from Pexels](https://www.pexels.com/video/a-man-and-a-woman-jogging-together-7876926/)


---
