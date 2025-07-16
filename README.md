# 🎨 ThermaToonPix

**ThermaToonPix** stands for **Thermal Vision**, **Cartoon**, and **Pixel Art Effects**.  
It is a lightweight and interactive media transformation tool that lets you apply cool visual effects — including heatmap simulation, cartoon-style rendering, and pixel art stylization — to **images**, **video files**, and **live webcam streams**.

Built with **OpenCV** for backend processing and **Streamlit** for an intuitive web-based interface.

🌐 **Try it live now**: [ThermaToonPix on Streamlit](https://thermatoonpix.streamlit.app)

---

## ✨ Features

- 🔥 **Thermal Vision** — Simulate thermal/infrared heatmap visuals
- 🖊️ **Cartoon Effect** — Apply stylized cartoon rendering with edge detection
- 🧱 **Pixel Art Effect** — Reduce resolution to generate retro pixel-style aesthetics
- ⚡ **Real-Time Processing** — Run everything directly in your browser, no need to install anything locally

---

## 🚀 Getting Started

### 📦 Installation

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install streamlit opencv-contrib-python-headless numpy Pillow streamlit-webrtc
```

---

### ▶️ Running the App

To launch ThermaToonPix locally:

```bash
streamlit run Homepage.py
```

> Make sure your webcam is connected if you want to try the live stream mode!

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) — frontend UI framework for interactive Python apps
- [OpenCV](https://opencv.org/) — computer vision backend for media transformation
- [NumPy](https://numpy.org/) — array-based processing
- [Pillow](https://python-pillow.org/) — image processing
- [streamlit-webrtc](https://github.com/whitphx/streamlit-webrtc) — real-time video/audio streaming via WebRTC

---

## 📬 Contact

Created by [Fernando Sutanto](https://github.com/Fernando889)  
Feel free to reach out with feedback or ideas!
