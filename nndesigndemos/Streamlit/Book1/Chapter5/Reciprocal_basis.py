import os
import streamlit as st
import base64
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff


path = os.getcwd()
css_path = f'{os.sep}'.join(path.split(sep=os.sep)[:-1]) + os.sep+ 'css'+ os.sep+ 'nnd.css'

import os
import streamlit as st
import base64
import numpy as np
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd


path = os.getcwd()
css_path = f'{os.sep}'.join(path.split(sep=os.sep)[:-1]) + os.sep+ 'css'+ os.sep+ 'nnd.css'

def run():

    # Use a raw string for the path
    def get_image_path(filename):
        return os.path.join("..", "Logo", filename)

    #Read svg file after finding the path
    def load_svg(svg_file):
        with open(svg_file, "r", encoding="utf-8") as f:
            svg = f.read()
        svg_base64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
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


    # Redirect to NND Chapters page
    if st.button('Back to NND Page'):
        st.session_state.page ='nnd'
        st.rerun()

    # Three column grids for header, chart and right side bar
    col1, col2, col3 = st.columns([9, 0.1, 4])
    with col3:
        # Side bar for Gram schmidt interactivity
        st.markdown(load_svg(get_image_path("Logo_Ch_6.svg")), unsafe_allow_html=True)
        st.markdown('<p class="content-font"> Reciprocal Basis, Chapter 6, Click [Expand] on the plot to define the basis {v1, v2}.'
                    'and the vector x to be expanded in terms of v1 and v2.'
                    '<br>'
                    '<br>'
                  ' Click [Expand] to expand a new vector. Click [Start] to start all over with a new basis. </p>',
                    unsafe_allow_html=True)
        st.button('Start', key=None, on_click=None, use_container_width=False)
        st.button('Expand', key=None, on_click=None, use_container_width=False)
        st.button('Clear all', key=None, on_click=None, use_container_width=False)


    with col2:
        st.markdown('<p class="content-font">'
                '<br>'
                '<br>'
                '<br>'
                '<br>'
                '</p>', unsafe_allow_html=True)
        st.markdown('<div class="vertical-line" style="height: 800px;"></div>', unsafe_allow_html=True)

    #Chapter Logo and header
    with col1:
        st.markdown("""
           <div style="display: flex; justify-content: space-between; align-items: center;">
               <div class="font" style="float: left;">
                   <span class="title-line"><em>Neural Network</em></span>
                   <span class="title-line">DESIGN</span>
               </div>
               <div class="header" style="float: right;">Chapter 6: Reciprocal basis</div>
           </div>
           """, unsafe_allow_html=True)
        st.markdown('<div class="blue-line"></div>', unsafe_allow_html=True)
        # Empty plot to initialize two vectors on click
        fig = go.Figure(go.Scatter(x=pd.Series(dtype=object), y=pd.Series(dtype=object), mode="markers"))

        button_x_list = []
        button_y_list = []
        button_graphs_list = []

        st.plotly_chart(fig)

    def draw_vectors():
        x, y = np.meshgrid(np.arange(-2, 2, .2),
                           np.arange(-2, 2, .2))
        u = np.cos(x) * y
        v = np.sin(x) * y

        # Create quiver figure
        fig = ff.create_quiver(x, y, u, v,
                               scale=.25,
                               arrow_scale=.4,
                               name='quiver',
                               line_width=1)
    def reciprocal_basis():
        pass
    def clear_all():
        pass


if __name__ == '__main__':
    run()