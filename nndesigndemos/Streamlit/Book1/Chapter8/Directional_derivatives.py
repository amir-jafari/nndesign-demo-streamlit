import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io


# Function to generate the surface plot and directional derivative
def generate_surface(x_lim, y_lim):
    x1 = np.linspace(x_lim[0], x_lim[1], 400)
    x2 = np.linspace(y_lim[0], y_lim[1], 400)
    X1, X2 = np.meshgrid(x1, x2)
    F = (X1 ** 2 + X2 ** 2) / 2  # Example function
    return X1, X2, F


# Convert Matplotlib figure to PIL Image
def fig_to_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    image = Image.open(buf)
    return image


# Plotting function for the function's contour
def plot_function_contour(X, Y, F):
    fig, ax = plt.subplots()
    CS = ax.contour(X, Y, F)
    ax.clabel(CS, inline=True, fontsize=8)
    ax.set_title('Function Contour')
    plt.close(fig)  # Prevent displaying the figure now
    return fig


# Setting up the function parameters
x_lim = [-4, 4]
y_lim = [-2, 2]
X, Y, F = generate_surface(x_lim, y_lim)
fig = plot_function_contour(X, Y, F)
background_image = fig_to_image(fig)

st.title("Directional Derivatives Interactive")

# Display the canvas for drawing
st.subheader("Draw a line to select direction for the directional derivative:")
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",  # Filler color
    stroke_width=2,
    stroke_color='#00008B',  # Dark Blue color for the line
    background_color="#eeeeee",
    background_image=background_image,
    update_streamlit=True,
    width=700,
    height=400,
    drawing_mode="line",
    key="canvas",
)

# Placeholder for displaying the selected direction or other messages
direction_placeholder = st.empty()

# Handle the canvas drawing data
if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
    # Extracting the last drawn line's start and end coordinates
    objects = canvas_result.json_data["objects"]
    last_object = objects[-1]
    start_x, start_y = last_object["x1"], last_object["y1"]
    end_x, end_y = last_object["x2"], last_object["y2"]

    # Placeholder calculation for directional derivative based on the line drawn
    # You'll need to implement the actual directional derivative calculation based on your function
    placeholder_directional_derivative = np.random.rand()  # This is a placeholder

    # Display the calculation result or any related message
    direction_placeholder.write(f"Directional derivative (placeholder value): {placeholder_directional_derivative:.2f}")


