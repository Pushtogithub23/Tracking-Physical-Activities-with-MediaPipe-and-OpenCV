# Tracking Physical Activities with MediaPipe and OpenCV

This repository contains a collection of projects focused on tracking various physical activities using computer vision, specifically integrating OpenCV with MediaPipe's Pose Estimation module and YOLOv8 for object detection. The projects utilize body landmarks and motion detection to track and count repetitions or actions from video inputs.

## Table of Contents

1. [Steps Tracker](#steps-tracker)
2. [Jumping Jacks Counter](#jumping-jacks-counter)
3. [Bench Press Counter](#bench-press-counter)
4. [Squats Counter](#squats-counter)
5. [Crunch Counter](#crunch-counter)
6. [Dumbbell Curl Counter](#dumbbell-curl-counter)
7. [Push-ups and Jump Counter](#push-ups-and-jump-counter)
8. [Steps Counter for Multiple People](#steps-counter-for-multiple-people)
9. [Rope Jump Workout Tracker](#rope-jump-workout-tracker)

---

## 1. Steps Tracker

This project is a step-tracking application that counts steps in a video by detecting and analyzing the motion of the right and left ankles. The system uses MediaPipe's Pose Estimation module to detect body landmarks and track leg movements for accurate step counting.

- **Technologies Used**: MediaPipe Pose Estimation, OpenCV
- **Functionality**: Tracks and counts steps based on ankle movements.
- **Input**: Video with walking sequences.
- **Output**: Annotated video with step count.

## 2. Jumping Jacks Counter

This project implements a jumping jacks counter using the MediaPipe pose estimation module integrated with OpenCV. The script detects body landmarks, calculates angles between key joints (shoulder, hip, elbow), and counts repetitions of jumping jacks based on arm movements.

- **Technologies Used**: MediaPipe Pose Estimation, OpenCV
- **Functionality**: Counts jumping jacks based on arm movements.
- **Input**: Video performing jumping jacks.
- **Output**: Annotated video with jumping jacks count.

## 3. Bench Press Counter

This project utilizes computer vision to count the number of bench press repetitions in a video using a pose estimation model. The program detects the position of key body landmarks (elbows and shoulders) and counts repetitions based on the movement of the elbow relative to the shoulder.

- **Technologies Used**: MediaPipe Pose Estimation, OpenCV
- **Functionality**: Tracks and counts bench press reps using elbow and shoulder movements.
- **Input**: Video of bench press exercise.
- **Output**: Annotated video with bench press rep count.

## 4. Squats Counter

This project uses computer vision and pose estimation to track and count squat repetitions in a video. It calculates joint angles, such as the knee and hip angles, to identify the up and down stages of a squat. The program displays the current rep count and joint angles on the video and saves the processed output.

- **Technologies Used**: MediaPipe Pose Estimation, OpenCV
- **Functionality**: Tracks squat reps by detecting knee and hip angles.
- **Input**: Video of squats exercise.
- **Output**: Annotated video with squat rep count and joint angles.

## 5. Crunch Counter

This project utilizes OpenCV and MediaPipe to count crunches performed in a video. The program processes video input, detects body landmarks, and calculates angles to determine the count of crunches. It visualizes the exercise count and angles on the video feed and saves the output to a new video file.

- **Technologies Used**: MediaPipe Pose Estimation, OpenCV
- **Functionality**: Tracks and counts crunches based on body landmark angles.
- **Input**: Video of crunch exercises.
- **Output**: Annotated video with crunch count and angle visualization.

## 6. Dumbbell Curl Counter

This project implements a dumbbell curl counter using OpenCV and MediaPipe for pose detection. The code analyzes video input to detect body landmarks, calculates the angles of the arms, and counts the number of repetitions based on the position of the arms. The output is a video annotated with the count of repetitions and angle measurements.

- **Technologies Used**: MediaPipe Pose Estimation, OpenCV
- **Functionality**: Counts dumbbell curls based on arm movement and angles.
- **Input**: Video of dumbbell curl exercises.
- **Output**: Annotated video with curl count and arm angle measurements.

## 7. Push-ups and Jump Counter

This project uses computer vision and pose estimation techniques to count push-ups and jumps performed by a user in a video. The implementation utilizes the MediaPipe library for pose detection, wrapped in a custom `PoseDetector` module. It calculates angles between key body landmarks to determine the current state of the exercise and updates counts accordingly.

- **Technologies Used**: MediaPipe Pose Estimation, OpenCV
- **Functionality**: Counts push-ups and jumps based on landmark movements and angles.
- **Input**: Video performing push-ups or jumps.
- **Output**: Annotated video with push-up and jump counts.

## 8. Steps Counter for Multiple People

This project demonstrates the integration of YOLO object detection with MediaPipe Pose Estimation to count the number of steps taken by people in a video. The code detects human subjects using YOLOv8, applies pose estimation to track their movements, and counts steps based on the movement of ankle landmarks.

- **Technologies Used**: YOLOv8, MediaPipe Pose Estimation, OpenCV
- **Functionality**: Tracks and counts steps for multiple people simultaneously.
- **Input**: Video containing multiple people walking.
- **Output**: Annotated video with individual step counts for each person.

## 9. Rope Jump Workout Tracker

This project is a Rope Jump Workout Tracker that uses a YOLOv8 model for object detection and tracking of people, along with counting their rope jumps in a video. The program calculates and displays the number of jumps for each tracked individual in real-time.

- **Technologies Used**: YOLOv8, MediaPipe Pose Estimation, OpenCV
- **Functionality**: Tracks and counts rope jumps for each person in real-time.
- **Input**: Video of people performing rope jump exercises.
- **Output**: Annotated video with rope jump counts for each tracked person.

---

## Installation

To get started with this repository, first clone the repo:

```bash
git clone https://github.com/Pushtogithub23/Tracking-Physical-Activities-with-MediaPipe-and-OpenCV.git
cd Tracking-Physical-Activities-with-MediaPipe-and-OpenCV
```

Then, install the necessary dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Each activity tracker can be run independently. Navigate to the corresponding folder and run the script:

```bash
python <script_name.py>
```

Make sure to provide the path to the video as needed within each script.

---

