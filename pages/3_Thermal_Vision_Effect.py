import streamlit as st
import cv2 as cv
import numpy as np
from PIL import Image
import tempfile
import os
import time
import platform
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase


def thermalVision(frame):
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (11, 11), cv.BORDER_DEFAULT)
    colorMap = cv.applyColorMap(blur, cv.COLORMAP_JET)
    return colorMap


class ThermalTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        return thermalVision(img)


st.set_page_config("ThermaToonPix", layout="centered")
st.title("🔥 ThermaToonPix - Thermal Vision Tool")


current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
os_info = platform.system()
st.markdown(f"🕒 **Time:** {current_time}")
st.markdown(f"💻 **OS:** {os_info}")
st.divider()


tabs = ["Image", "Video", "Live"]
tab1, tab2, tab3 = st.columns(3)

if "tab" not in st.session_state:
    st.session_state.tab = "Image"

with tab1:
    if st.button("🖼 Image"):
        st.session_state.tab = "Image"
with tab2:
    if st.button("📼 Video"):
        st.session_state.tab = "Video"
with tab3:
    if st.button("🎥 Live"):
        st.session_state.tab = "Live"
st.divider()


if st.session_state.tab == "Image":
    st.subheader("🖼 Upload Image")
    uploaded_file = st.file_uploader(
        "Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(image)
        img_bgr = cv.cvtColor(img_np, cv.COLOR_RGB2BGR)

        start = time.time()
        thermal_img = thermalVision(img_bgr)
        elapsed = time.time() - start

        st.image(cv.cvtColor(thermal_img, cv.COLOR_BGR2RGB),
                 caption="Thermal Vision Image", use_container_width=True)
        st.success(f"✅ Processed in {elapsed:.2f} seconds")

        out_path = "thermal_image.png"
        cv.imwrite(out_path, thermal_img)
        with open(out_path, "rb") as f:
            st.download_button("💾 Download", f, file_name="thermal_image.png")


elif st.session_state.tab == "Video":
    st.subheader("📼 Upload Video")
    video_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

    if video_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())
        input_path = tfile.name

        cap = cv.VideoCapture(input_path)
        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        out_path = "thermal_output.mp4"
        out = None
        frame_count = 0

        st.info("Processing video...")

        start = time.time()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            thermal_frame = thermalVision(frame)
            if out is None:
                h, w, _ = thermal_frame.shape
                out = cv.VideoWriter(out_path, fourcc, 20.0, (w, h))
            out.write(thermal_frame)
            frame_count += 1

        cap.release()
        out.release()
        elapsed = time.time() - start

        st.video(out_path)
        st.success(
            f"✅ Processed {frame_count} frames in {elapsed:.2f} seconds")
        with open(out_path, "rb") as f:
            st.download_button("💾 Download", f, file_name="thermal_output.mp4")


elif st.session_state.tab == "Live":
    st.subheader("🎥 Live Thermal Camera")
    try:
        webrtc_streamer(
            key="live_thermal",
            video_transformer_factory=ThermalTransformer,
            media_stream_constraints={"video": True, "audio": False},
            async_transform=True
        )
        st.info("✅ If webcam doesn't appear, check browser permissions.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
