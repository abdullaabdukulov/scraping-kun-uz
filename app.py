import streamlit as st
# import plotly as plt
from PIL import Image
from kun_uz import _main
import urllib.request


def add_logo(logo_path, width, height):
    # url = urllib.request.urlretrieve(logo_path, 'logo.png')
    logo = Image.open('logo.png')
    modified_logo = logo.resize((width, height))
    return modified_logo


def main_page():
    st.sidebar.image(add_logo('logo.png', width=100, height=80))
    st.sidebar.markdown("# Tanlang 🔎")
    with st.sidebar:
        with st.form(key='my_form'):
            # st.write("Inside the form")
            slider_val = st.slider("Qaysi yangilik?", max_value=25)
            # Every form must have a submit button.
            submitted = st.form_submit_button("Submit")
            if submitted:
                # st.write("slider", slider_val)
                son = True
    # st.sidebar.number_input('enter', step=1, max_value=20, min_value=1)
    if slider_val == 0:
        st.markdown("<h2 style='text-align: left; color: blue'>Eng So'nggi Yanglik</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2 style='text-align: left; color: blue'>Eng So'nggi {slider_val} Yanglik</h2>", unsafe_allow_html=True)

    st.markdown("""<style>
    .css-k1vhr4 
    {
    display: block;
    margin: 60px;
    }
    .css-hxt7ib {
    padding-top: 2rem;
    padding-left: 1rem;
    padding-right: 1rem;
}
    .css-hxt7ib h1 {
    font-size: 2.5rem;
    font-weight: 600;
}
                </style>""", unsafe_allow_html=True)
    left, middle, right = st.columns((2, 5, 2))
    if slider_val is None:
        with left:
            st.plotly_chart(_main(0), use_container_width=False)
    else:
        st.plotly_chart(_main(slider_val), use_container_width=False)


main_page()