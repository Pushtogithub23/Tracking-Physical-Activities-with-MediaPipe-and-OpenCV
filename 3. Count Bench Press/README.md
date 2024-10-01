# Bench Press Repetition Counter using MediaPipe's Pose Landmarks

This project utilizes computer vision to count the number of bench press repetitions in a video using a pose estimation model. The program detects the position of key body landmarks (elbows and shoulders) and counts repetitions based on the movement of the elbow relative to the shoulder.

![bench_press_counter](https://github.com/user-attachments/assets/43f4f218-7f08-47eb-a34b-e0fcaa01db61)


## Features

- Detects and tracks the user's pose during a bench press.
- Automatically counts the number of repetitions performed.
- Displays the count and the state (up or down) directly on the video.
- Saves the processed video with the rep counter as output.

## Dependencies

To run this project, you need to install the following libraries:

- OpenCV: Used for video processing and visualization.
- MediaPipe: For detecting required Pose Landmarks(Elbow, Wrist Shoulder etc.)
- Utility functions: A custom module for drawing text with a background (`draw_text_with_bg`).

### Installation

You can install the dependencies using the following:

```bash
pip install opencv-python mediapipe
```

Ensure you also have the custom modules available in the project folder:

- `Pose_estimationModule.py` (PoseDetector class for pose detection)
- `utils.py` (for drawing text with a background on the frame)

## How It Works

1. The program reads the input video and uses a pose detection model to identify key landmarks such as the elbows and shoulders.
2. It counts repetitions by detecting the movement of the elbow above and below the shoulder, indicating an up and down movement typical of a bench press.
3. The repetition count is displayed on the video in real-time, and the color changes based on the state:
   - Red for the "down" position (elbow below the shoulder).
   - Green for the "up" position (elbow above the shoulder).
4. The processed video with the rep counter is saved as output.

## File Structure

```
📂 VIDEOS
 ┣ 📂 INPUTS
 ┃ ┗ bench_press.mp4         # Input video for processing
 ┣ 📂 OUTPUTS
 ┃ ┗ bench_press_counter.mp4  # Output video with rep counter
📜 Pose_estimationModule.py   # Pose detection module
📜 utils.py                   # Utility functions for text drawing
📜 main.py                    # Main script for counting reps
```

## Usage

1. Place the input video file (`bench_press.mp4`) in the `VIDEOS/INPUTS/` directory.
2. Run the `main.py` script:

```bash
python main.py
```

3. The program will process the video and generate an output file `bench_press_counter.mp4` in the `VIDEOS/OUTPUTS/` folder with the rep count overlay.

## Customization

- **Input video**: Modify the video path in the script to use a different video file.
- **Landmark Detection**: The script uses key body landmarks for counting repetitions. You can adjust the detection logic if working with different exercises.
- **Thresholds**: The thresholds for detecting "up" and "down" positions can be adjusted in the `update_count_and_color()` function based on your requirements.


## References
1. [MediaPipe's article on Pose Landmarks Detection](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker)
2. [Video by Antoni Shkraba from Pexels](https://www.pexels.com/video/a-man-lifting-weights-on-a-bench-press-machine-4921647/)

---
