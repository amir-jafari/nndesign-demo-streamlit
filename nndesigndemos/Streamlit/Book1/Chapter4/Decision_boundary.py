import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import Perceptron


# Function to update and plot decision boundary, points, and calculate error
def update_plot():
    fig, ax = plt.subplots()
    # Plot points
    for point in st.session_state.data:
        if point[2] == 1:  # Positive class
            ax.plot(point[0], point[1], 'go')
        else:  # Negative class
            ax.plot(point[0], point[1], 'ro')

    # Fit Perceptron and plot decision boundary if possible
    if len(st.session_state.data) > 0:
        X = np.array(st.session_state.data)[:, :2]
        y = np.array(st.session_state.data)[:, 2]
        clf = Perceptron(tol=1e-3, random_state=0)
        clf.fit(X, y)
        coef = clf.coef_[0]
        intercept = clf.intercept_
        x_values = np.linspace(-5, 5, 100)
        y_values = -(coef[0] / coef[1]) * x_values - (intercept / coef[1])
        ax.plot(x_values, y_values, 'r--')

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    st.pyplot(fig)


# Initialize session state variables
if 'data' not in st.session_state:
    st.session_state.data = []

# Sidebar for adding points
with st.sidebar:
    st.title("Controls")
    x = st.number_input('X coordinate', value=0.0, step=0.1)
    y = st.number_input('Y coordinate', value=0.0, step=0.1)
    point_class = st.selectbox('Class', options=[1, 0], format_func=lambda x: "Positive" if x == 1 else "Negative")
    add_point = st.button("Add point")
    clear_data = st.button("Clear Data")

if add_point:
    st.session_state.data.append([x, y, point_class])

if clear_data:
    st.session_state.data = []

# Main plot
update_plot()

# Placeholder for additional functionality and instructions
st.write("Add points using the controls on the left. The decision boundary is updated based on the points added.")
