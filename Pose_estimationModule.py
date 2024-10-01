import cv2 as cv
import mediapipe as mp
import os


class PoseDetector:
    def __init__(self, mode=False, complexity=1, smooth=True, detection_con=0.5, track_con=0.5):
        self.results = None
        self.mode = mode
        self.complexity = complexity
        self.smooth = smooth
        self.detection_con = detection_con
        self.track_con = track_con

        self.mpPose = mp.solutions.pose
        # Correctly initialize Pose with appropriate arguments
        self.pose = self.mpPose.Pose(
            static_image_mode=self.mode,
            model_complexity=self.complexity,
            smooth_landmarks=self.smooth,
            min_detection_confidence=self.detection_con,
            min_tracking_confidence=self.track_con
        )
        self.mpDraw = mp.solutions.drawing_utils

    def find_pose(self, frame, draw=True):
        # Convert frame to RGB for MediaPipe processing
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # Process the frame to detect poses
        self.results = self.pose.process(frame_rgb)

        # Draw the detected pose landmarks on the frame
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(frame, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return frame

    def get_positions(self, frame):
        # Extract pose landmark positions and store them in a dictionary
        landmarks = {}
        if self.results.pose_landmarks:
            for ID, landmark in enumerate(self.results.pose_landmarks.landmark):
                # Convert normalized coordinates to pixel coordinates
                h, w, c = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                landmarks[ID] = (cx, cy)
        return landmarks


def pose_estimator_in_video(video_path, filename, resizing_factor, save_video=False):
    # Initialize video capture from file or webcam
    cap = cv.VideoCapture(0 if video_path == 0 else video_path)
    if not cap.isOpened():
        print("Couldn't capture the video file")
        return

    # Read the first frame to determine video properties
    ret, frame = cap.read()
    if not ret:
        print("Error reading the video file.")
        return

    # Get frame dimensions and FPS
    frame_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    fps = int(cap.get(cv.CAP_PROP_FPS))

    # Create an instance of the PoseDetector class
    detector = PoseDetector()

    # Setup for saving video if enabled
    if save_video:
        video_dir = r"D:\PyCharm\PyCharm_files\MEDIAPIPE\POSE_ESTIMATION\VIDEOS"
        save_video_path = os.path.join(video_dir, filename)
        fourcc = cv.VideoWriter_fourcc(*'mp4v')  # Define codec
        out = cv.VideoWriter(save_video_path, fourcc, fps, (frame_width, frame_height))

    # Calculate resized frame dimensions
    resized_frame_size = (int(resizing_factor * frame_width), int(resizing_factor * frame_height))

    # Process video frames
    while cap.isOpened():
        ret, frame = cap.read()  # Read frame from video capture
        if not ret:
            break

        # Detect poses in the current frame
        frame = detector.find_pose(frame)
        landmarks = detector.get_positions(frame)

        # Print detected landmarks
        # if len(landmarks) > 0:
        #     print(landmarks)

        # Save the processed frame to video file if enabled
        if save_video:
            out.write(frame)

        # Flip frame horizontally if using webcam
        if video_path == 0:
            frame = cv.flip(frame, 1)

        # Resize frame for display
        resized_frame = cv.resize(frame, resized_frame_size)
        cv.imshow('Video', resized_frame)  # Display the frame
        if cv.waitKey(1) & 0xff == ord('p'):  # Exit on pressing 'p'
            break

    # Release resources
    cap.release()
    if save_video:
        out.release()
    cv.destroyAllWindows()


def main():
    # Inputs
    video_path = input("Enter video path or '0' for webcam: ").strip().strip('"').strip("'")
    resizing_factor = float(input("Enter resizing factor (e.g., 0.5 for 50%): "))
    save_video = input("Do you want to save the video? (yes or no): ").lower() == 'yes'

    filename = None  # Initialize filename
    if save_video:
        filename = input("Enter filename to save the video: ")

    # Convert video_path to 0 if it's meant to be the webcam
    if video_path == '0':
        video_path = 0

    print(f"Video path is: {video_path}")  # Debug print to check path

    pose_estimator_in_video(video_path, filename, resizing_factor, save_video)


if __name__ == "__main__":
    main()
