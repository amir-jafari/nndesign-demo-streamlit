import streamlit as st
import Landingpage
import NND_Page
from Book1.Chapter2 import One_input_neuron
from Book1.Chapter2 import Two_input_neuron
from Book1.Chapter3 import Hamming_classification
from Book1.Chapter5 import Gram_schmidt


# Initialize session state for page navigation
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# Function to load a page based on session state
def load_page(page_name):
    if page_name == 'landing':
        Landingpage.run()
    elif page_name == 'nnd':
        NND_Page.run()
    elif page_name == "One_input_neuron":
        One_input_neuron.run()
    elif page_name == "Two_input_neuron":
        Two_input_neuron.run()
    elif page_name == 'Hamming_classification':
        Hamming_classification.run()
    elif page_name == "Gram_schmidt":
        Gram_schmidt.run()
    # Add more pages for the different demos as elif blocks here

#Load the current page
load_page(st.session_state.page)