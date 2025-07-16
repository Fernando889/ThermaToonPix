import streamlit as st
import os

st.set_page_config(page_title='ThermaToonPix', layout='centered')
st.title('🎨 Introducing ThermaToonPix')
st.divider()

st.write(
    'ThermaToonPix stands for Thermal Vision, Cartoon, and Pixel Art Effects. '
    'It is an interactive and simple media transformation tool that allows users to apply '
    'thermal vision, cartoon-style, and pixel art effects to images, video files, and live webcam streams. '
    'Built entirely with OpenCV for Backend processing and Streamlit for the UI (User Interface).'
)
st.divider()

st.markdown('### ✨ Key Features:')
st.markdown("""
1. 🔥 Apply simple **Thermal Vision** filters to simulate heatmaps  
2. 🖊️ Convert visuals into simple **Cartoon Effects**  
3. 🧱 Transform visuals into simple **Pixel Art Effects**  
4. ⚡ Experience it all **in real-time**, right in your browser — no installation needed!
""")
st.divider()

st.markdown('### 🧪 Visual Examples:')

with st.container():
    st.write('Cartoon Effect')
    st.image(os.path.join("static", "Ferrari Daytona Cartoon.png"))
    st.caption("Source Photo: Pinterest")
    if st.button("Go to Cartoon Effect"):
        st.switch_page("pages/1_Cartoon_Effect.py")

with st.container():
    st.write('Pixel Art Effect')
    st.image(os.path.join("static", "pixel_art.jpg"))
    st.caption("Source Photo: Pinterest")
    if st.button("Go to Pixel Art Effect"):
        st.switch_page("pages/2_Pixel_Art_Effect.py")

with st.container():
    st.write("Thermal Vision Effect")
    st.image(os.path.join("static", "people.jpg"))
    st.caption("Source Photo: Pinterest")
    if st.button("Go to Thermal Vision Effect"):
        st.switch_page("pages/3_Thermal_Vision_Effect.py")
