import av
import cv2
import mediapipe as mp
import streamlit as st
from streamlit_webrtc import webrtc_streamer

mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

st.title("StreamLit + MediaPipe demo")
st.write("Face Detection")


class VideoProcessor:
    def __init__(self) -> None:
        self.min_confidence = 50

    def recv(self, frame):
        with mp_face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=(self.min_confidence / 100),
        ) as face_detection:
            img = frame.to_ndarray(format="bgr24")
            img.flags.writeable = False
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = face_detection.process(img)

            # Draw the face detection annotations on the image.
            img.flags.writeable = True
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(img, detection)
            img = cv2.flip(img, 1)
            return av.VideoFrame.from_ndarray(img, format="bgr24")


ctx = webrtc_streamer(key="example", video_processor_factory=VideoProcessor)
if ctx.video_processor:
    ctx.video_processor.min_confidence = st.slider(
        "Confidence[%]",
        min_value=0,
        max_value=100,
        step=1,
        value=50,
    )
