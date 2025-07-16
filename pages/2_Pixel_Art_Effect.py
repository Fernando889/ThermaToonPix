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


def pixelate(frame, pixel_size=8, num_colors=16):
    height, width = frame.shape[:2]
    temp = cv.resize(frame, (width // pixel_size, height //
                             pixel_size), interpolation=cv.INTER_AREA)

    data = temp.reshape((-1, 3)).astype(np.float32)
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 20, 1.0)
    _, labels, centers = cv.kmeans(
        data, num_colors, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
    quantized = centers[labels.flatten()].reshape(temp.shape).astype(np.uint8)

    pixelated = cv.resize(quantized, (width, height),
                          interpolation=cv.INTER_NEAREST)
    return pixelated


class PixelArtTransformer(VideoTransformerBase):
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        pixel = pixelate(img, pixel_size=20, num_colors=16)
        return pixel


st.set_page_config("ThermaToonPix", layout="centered")
st.title("🧩 ThermaToonPix - Pixel Art Effect Tool")


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
        pixel_img = pixelate(img_bgr, pixel_size=20, num_colors=16)
        elapsed = time.time() - start

        st.image(cv.cvtColor(pixel_img, cv.COLOR_BGR2RGB),
                 caption="Pixelated Image", use_container_width=True)
        st.success(f"✅ Processed in {elapsed:.2f} seconds")

        out_path = "pixel_image.png"
        cv.imwrite(out_path, pixel_img)
        with open(out_path, "rb") as f:
            st.download_button("💾 Download", f, file_name="pixel_image.png")


elif st.session_state.tab == "Video":
    st.subheader("📼 Upload Video")
    video_file = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])

    if video_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(video_file.read())
        input_path = tfile.name

        cap = cv.VideoCapture(input_path)
        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        out_path = "pixel_output.mp4"
        out = None
        frame_count = 0

        st.info("Processing video...")

        start = time.time()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            pixel_frame = pixelate(frame, pixel_size=20, num_colors=16)
            if out is None:
                h, w, _ = pixel_frame.shape
                out = cv.VideoWriter(out_path, fourcc, 20.0, (w, h))
            out.write(pixel_frame)
            frame_count += 1

        cap.release()
        out.release()
        elapsed = time.time() - start

        st.video(out_path)
        st.success(
            f"✅ Processed {frame_count} frames in {elapsed:.2f} seconds")
        with open(out_path, "rb") as f:
            st.download_button("💾 Download", f, file_name="pixel_output.mp4")


elif st.session_state.tab == "Live":
    st.subheader("🎥 Live Pixel Art Camera")
    try:
        webrtc_streamer(
            key="live_pixel",
            video_transformer_factory=PixelArtTransformer,
            media_stream_constraints={"video": True, "audio": False},
            async_transform=True
        )
        st.info("✅ If webcam doesn't appear, check browser permissions.")
    except Exception as e:
        st.error(f"❌ Error: {e}")
