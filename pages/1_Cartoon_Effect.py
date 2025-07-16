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


def cartoonEffect(frame):
    num_down = 2
    num_bilateral = 7

    img_color = frame.copy()
    for _ in range(num_down):
        img_color = cv.pyrDown(img_color)

    for _ in range(num_bilateral):
        img_color = cv.bilateralFilter(
            img_color, d=9, sigmaColor=9, sigmaSpace=7)

    for _ in range(num_down):
        img_color = cv.pyrUp(img_color)

    if img_color.shape != frame.shape:
        img_color = cv.resize(img_color, (frame.shape[1], frame.shape[0]))

    img_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    img_blur = cv.medianBlur(img_gray, 7)

    img_edge = cv.adaptiveThreshold(img_blur, 255,
                                    cv.ADAPTIVE_THRESH_MEAN_C,
                                    cv.THRESH_BINARY, 9, 2)
    img_edge = cv.cvtColor(img_edge, cv.COLOR_GRAY2BGR)

    cartoon = cv.bitwise_and(img_color, img_edge)
    return cartoon


class CartoonTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        cartoon = cartoonEffect(img)
        return cartoon


st.set_page_config("ThermaToonPix", layout="centered")
st.title("🎨 ThermaToonPix - Cartoon Effect Tool")


current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
os_info = platform.system()
st.markdown(f"🕒 **Date & Time:** {current_time}")
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
        cartoon = cartoonEffect(img_bgr)
        elapsed = time.time() - start

        st.image(cv.cvtColor(cartoon, cv.COLOR_BGR2RGB),
                 caption="Cartoonized Image", use_container_width=True)
        st.success(f"✅ Processed in {elapsed:.2f} seconds")

        out_path = "cartoon_image.png"
        cv.imwrite(out_path, cartoon)
        with open(out_path, "rb") as f:
            st.download_button("💾 Download", f, file_name="cartoon_image.png")


elif st.session_state.tab == "Video":
    st.subheader("📼 Upload Video")
    video_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

    if video_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())
        input_path = tfile.name

        cap = cv.VideoCapture(input_path)
        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        out_path = "cartoon_output.mp4"
        out = None
        frame_count = 0

        st.info("Processing video...")

        start = time.time()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            cartoon = cartoonEffect(frame)
            if out is None:
                h, w, _ = cartoon.shape
                out = cv.VideoWriter(out_path, fourcc, 20.0, (w, h))
            out.write(cartoon)
            frame_count += 1

        cap.release()
        out.release()
        elapsed = time.time() - start

        st.video(out_path)
        st.success(
            f"✅ Processed {frame_count} frames in {elapsed:.2f} seconds")
        with open(out_path, "rb") as f:
            st.download_button("💾 Download", f, file_name="cartoon_output.mp4")

elif st.session_state.tab == "Live":
    st.subheader("🎥 Live Cartoon Camera")
    try:
        webrtc_streamer(
            key="live_cartoon",
            video_transformer_factory=CartoonTransformer,
            media_stream_constraints={"video": True, "audio": False},
            async_transform=True
        )
        st.info("✅ If webcam doesn't appear, check browser permissions.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
