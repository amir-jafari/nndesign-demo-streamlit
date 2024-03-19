import streamlit as st
from streamlit_drawable_canvas import st_canvas
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io

# Function to generate the Taylor series terms for a single order
def generate_single_order_taylor_series(x0, x_points, order):
    y0 = np.cos(x0)
    if order == 0:
        return np.ones_like(x_points) * y0
    elif order == 1:
        return -(x_points - x0) * np.sin(x0)
    elif order == 2:
        return (x_points - x0) ** 2 * np.cos(x0) / 2
    elif order == 3:
        return -(x_points - x0) ** 3 * np.sin(x0) / 6
    elif order == 4:
        return (x_points - x0) ** 4 * np.cos(x0) / 24
    else:
        return np.zeros_like(x_points)

# Convert Matplotlib figure to PIL Image
def fig_to_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.0)
    buf.seek(0)
    image = Image.open(buf)
    return image

# Plotting function for the cosine function
def plot_cosine_function(x_points):
    fig, ax = plt.subplots()
    ax.plot(x_points, np.cos(x_points), label='cos(x)', linestyle='--')
    ax.set_xlim([-6, 6])
    ax.set_ylim([-2, 2])
    ax.grid(True)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    return fig_to_image(fig)

st.title("Interactive Taylor Series Approximation")

st.subheader("Click on the plot to choose a point for Taylor series approximation:")
x_points = np.linspace(-6, 6, 400)
cosine_plot_image = plot_cosine_function(x_points)

canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.3)",
    stroke_width=0,
    background_image=cosine_plot_image,
    update_streamlit=True,
    width=700,
    height=400,
    drawing_mode="point",
    key="cosine_canvas",
)

if canvas_result.json_data is not None and len(canvas_result.json_data["objects"]) > 0:
    points = canvas_result.json_data["objects"]
    x0 = points[0]["left"] / 700 * 12 - 6

    st.write(f"You selected x = {x0:.2f}")

    # Multiselect for order selection
    order_options = ["Order 0", "Order 1", "Order 2", "Order 3", "Order 4"]
    selected_orders = st.multiselect("Select the orders of the Taylor series approximation:", order_options, default=["Order 0"])

    # Plotting the selected Taylor series approximations
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(x_points, np.cos(x_points), 'k--', label='cos(x)')

    for order_name in selected_orders:
        order = int(order_name.split()[-1])
        approximation = np.cumsum([generate_single_order_taylor_series(x0, x_points, i) for i in range(order + 1)], axis=0)[-1]
        ax.plot(x_points, approximation, label=f'Taylor Series - {order_name}')

    ax.plot(x0, np.cos(x0), 'ro', label='Selected Point')
    ax.set_xlim([-6, 6])
    ax.set_ylim([-2, 2])
    ax.grid(True)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    st.pyplot(fig)





