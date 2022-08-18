import streamlit as st
from PIL import Image
import numpy as np
import av
import cv2
from streamlit_webrtc import (
    RTCConfiguration,
    WebRtcMode,
    WebRtcStreamerContext,
    webrtc_streamer,
)

# PAGE CONFIGURATION --------------------------------------------------------------------------------------------------
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)
st.set_page_config(
       layout='centered',  # 'centered' or 'wide'
       initial_sidebar_state="collapsed",
       menu_items=None)


# CALLBACK DEFINITION -------------------------------------------------------------------------------------------------
def callback(frame: av.VideoFrame) -> av.VideoFrame:
    img = frame.to_ndarray(format="bgr24")
    img = np.flip(img, axis=1).astype(np.uint8)

    return av.VideoFrame.from_ndarray(img, format="bgr24")


# APPLICATION --------------------------------------------------------------------------------------------------
cols = st.columns([1, 3, 1])
cols[1].write(' ')

st.markdown('WebRTC Demo', unsafe_allow_html=True)

webrtc_ctx = webrtc_streamer(
    key="emotion_recognition",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    desired_playing_state=True,
    video_frame_callback=callback,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True
)
