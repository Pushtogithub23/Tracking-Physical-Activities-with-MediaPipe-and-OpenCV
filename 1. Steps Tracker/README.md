# Step Tracker using MediaPipe's Pose Estimation

This project is a **step-tracking application** that counts steps in a video by detecting and analyzing the motion of the right and left ankles. The system uses **MediaPipe's Pose Estimation** module to detect body landmarks and track leg movement to count the steps accurately.

![steps_tracker](https://github.com/user-attachments/assets/0e8a82a3-46a8-4a4b-9b23-381ace20c56a)


## Features

- **Pose Detection**: Uses MediaPipe's Pose Estimation to detect body landmarks, particularly focusing on the ankle points.
- **Step Counting**: Tracks the motion of the ankles to determine whether the user is stepping with the left or right leg.
- **Real-time Video Processing**: The video is processed frame by frame to track the number of steps taken by the person in the video.
- **Customizable Output**: The processed video with the step count displayed is saved to an output file.
- **Display with OpenCV**: Optionally shows the video with step count overlay in real-time.

## Dependencies

- Python 3.11
- OpenCV (`cv2`)
- NumPy (`numpy`)
- [MediaPipe](https://ai.google.dev/edge/mediapipe/solutions/guide)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Pushtogithub23/Tracking-Physical-Activities-with-MediaPipe-and-OpenCV.git
   cd 1. Steps Tracker
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   Ensure `MediaPipe` is installed for pose detection:

   ```bash
   pip install mediapipe
   ```

3. Prepare your input video:

   Place your input video in the `VIDEOS/INPUTS` folder and rename it (e.g., `running_2.mp4`) or adjust the filename in the script accordingly.

## Usage

To run the step tracker, execute the following command in your terminal:

```bash
python step_tracker.py
```

The script will:

1. Open the input video and initialize pose detection.
2. Detect and count steps based on the ankle positions (right and left ankles).
3. Display the processed video in real-time with the step count overlay.
4. Save the output video with step count annotations to the `VIDEOS/OUTPUTS` directory.

You can exit the video display by pressing the `p` key.

### Customizing the Video Output

- **Input Video**: The input video can be changed by modifying the path in the `cv.VideoCapture()` function.
- **Output Video**: You can set a different filename or location for the output video by modifying the `filename` variable.

## Project Structure

```
step-tracker/
│
├── VIDEOS/
│   ├── INPUTS/
│   │   └── running_2.mp4        # Sample input video
│   └── OUTPUTS/
│       └── steps_tracker.mp4    # Output video with step count
│
├── utils.py                     # Utility functions (e.g., for drawing text with background)
├── Pose_estimationModule.py      # Pose detection module based on MediaPipe
├── step_tracker.py               # Main script for step tracking
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

## How It Works

The step-tracking algorithm works by identifying the movement of the ankles. Specifically, it:

1. **Detects Pose Landmarks**: Using MediaPipe's Pose Estimation to get landmarks, focusing on the right and left ankles.
2. **Step Detection Logic**: The system checks the vertical positions of the ankles to detect when one ankle moves above the other, indicating a step.
3. **Counting Steps**: A step is counted when one ankle moves above the other, updating the step count and stage (whether it's the right or left leg stepping up).

## References
1. [MediaPipe's article on Pose Landmarks detection](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)
2. [Video by RDNE Stock project from Pexels](https://www.pexels.com/video/video-of-a-man-training-football-7187055/)

---
