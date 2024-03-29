import os
import base64
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def run():
    def load_svg(svg_file):
        with open(svg_file, "r", encoding="utf-8") as f:
            svg = f.read()
        svg_base64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
        # Adjust 'max-width' to increase the size of the image, for example, to 60% of its container
        # You can also adjust 'height' if necessary, but 'auto' should maintain the aspect ratio
        svg_html = f'''
        <div style="text-align: center; width: 100%;">
            <img src="data:image/svg+xml;base64,{svg_base64}" alt="SVG Image" style="max-width: 80%; height: 150px; margin: 20px;">
        </div>
        '''
        return svg_html

        # Set the layout to "wide"
        st.set_page_config(layout="wide")

        #Load css file
        def load_css(file_name="../css/nnd.css"):
            with open(file_name) as f:
                css_file = f'<style>{f.read()}</style>'
            return css_file

        css = load_css()
        st.markdown(css, unsafe_allow_html=True)

        if st.button('Back to NND Page'):
            st.session_state.page = 'nnd'
            st.rerun()

        # Define the relative path for the images using a raw string
        image_path = "../Chapters"
        def get_image_path(filename):
            return os.path.join(image_path, filename)


        def purelin(n): return n
        def poslin(n): return np.maximum(0, n)
        def hardlim(n): return np.where(n >= 0, 1, 0)
        def hardlims(n): return np.where(n >= 0, 1, -1)
        def satlin(n): return np.minimum(np.maximum(0, n), 1)
        def satlins(n): return np.minimum(np.maximum(-1, n), 1)
        def logsig(n): return 1 / (1 + np.exp(-n))
        def tansig(n): return np.tanh(n)

        transfer_functions = {
            "purelin": purelin,
            "poslin": poslin,
            "hardlim": hardlim,
            "hardlims": hardlims,
            "satlin": satlin,
            "satlins": satlins,
            "logsig": logsig,
            "tansig": tansig
        }


        #Create 3 col grids on the page with grid sizes 9, 0.1, 3
        col1, col2, col3 = st.columns([9, 0.1, 3])

        with col3:
            st.markdown(load_svg(get_image_path("3/Logo_Ch_2.svg")), unsafe_allow_html=True)
            st.markdown('<p class="content-font">"Click [Go] to send a fruit down the belt to be classified"'
                        '<br>'
                        ' by a Hamming network. The calculations for the Hamming network will appear below'
                        '</p>', unsafe_allow_html=True)

            st.markdown('<p class="content-font">Weight (w):</p>', unsafe_allow_html=True)
            weight = st.slider("", min_value=-3.0, max_value=3.0, value=1.0, step=0.1, key="weight")

            st.markdown('<p class="content-font">Bias (b):</p>', unsafe_allow_html=True)
            bias = st.slider("", min_value=-3.0, max_value=3.0, value=0.0, step=0.1, key="bias")

            st.markdown('<p class="content-font">Transfer Function (f):</p>', unsafe_allow_html=True)
            selected_function = st.selectbox("", options=list(transfer_functions.keys()))

        with col2:
            st.markdown('<p class="content-font">'
                        '<br>'
                        '<br>'
                        '<br>'
                        '<br>'
                        '</p>', unsafe_allow_html=True)
            st.markdown('<div class="vertical-line" style="height: 800px;"></div>', unsafe_allow_html=True)

        with col1:
            st.markdown("""
                   <div style="display: flex; justify-content: space-between; align-items: center;">
                       <div class="font" style="float: left;">
                           <span class="title-line"><em>Neural Network</em></span>
                           <span class="title-line">DESIGN</span>
                       </div>
                       <div class="header" style="float: right;">Chapter 3: Hamming Classification</div>
                   </div>
                   """, unsafe_allow_html=True)

            st.markdown('<div class="blue-line"></div>', unsafe_allow_html=True)
            st.markdown(load_svg("../Figures/nn2d3d1_1.svg"), unsafe_allow_html=True)


if __name__ == "__main__":
    run()