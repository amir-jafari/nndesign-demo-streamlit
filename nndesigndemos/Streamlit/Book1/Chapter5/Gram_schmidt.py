import os
import streamlit as st
import base64
import numpy as np
import plotly.graph_objects as go
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
        st.markdown(load_svg(get_image_path("Logo_Ch_5.svg")), unsafe_allow_html=True)
        st.markdown('<p class="content-font"> Gram-Schmidt, Chapter 5, Click [Start] to begin. Click twice in '
                    'the top graph to create two vectors to be orthogonalized.'
                    '<br>'
                    '<br>'
                  ' Then click [Compute] to see the orthogonal vectors. Click [Clear] again to clear all and repeat. </p>',
                    unsafe_allow_html=True)
        st.button('Start', key=None, on_click=None, use_container_width=False)
        st.button('Compute', key=None, on_click=None, use_container_width=False)
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
               <div class="header" style="float: right;">Chapter 5: Gram-Schmidt</div>
           </div>
           """, unsafe_allow_html=True)
        st.markdown('<div class="blue-line"></div>', unsafe_allow_html=True)

        # Initialize empty lists to store coordinates
        x_coords = []
        y_coords = []

        # Define a callback function to handle click events
        def handle_click(trace, points, selector):
            if points.point_inds:
                # Get the coordinates of the clicked point
                x = points.xs[0]
                y = points.ys[0]

                # Append coordinates to lists
                x_coords.append(x)
                y_coords.append(y)

                # Update scatter plot with the new vector
                fig.add_trace(go.Scatter(x=[0, x], y=[0, y], mode='lines', name='Original Vector'))

        # Create an empty scatter plot
        fig = go.Figure()

        # Add scatter plot with click event handling
        fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(color='blue'), opacity=0, name='Click Here'))

        # Update layout
        fig.update_layout(
            title="Click on the graph to draw a vector",
            xaxis=dict(title="X"),
            yaxis=dict(title="Y"),
        )

        # Assign callback function to scatter plot
        fig.data[0].on_click(handle_click)

        # Display the figure using Streamlit
        st.plotly_chart(fig)

        # Display the coordinates
        st.write("Clicked Coordinates:")
        st.write("X:", x_coords)
        st.write("Y:", y_coords)

    def gram_schmidt():
        pass
    def clear_all():
        pass


if __name__ == '__main__':
    run()