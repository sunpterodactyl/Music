import streamlit as st
from text import encode_message, decode_message
from PIL import Image
import logging
from logging import getLogger
import numpy as np
#TODO: Reload encode section to work with session_state
#TODO: 

st.title('Image Steganography')

print("---------------------------")
app_logger = getLogger()
app_logger.addHandler(logging.StreamHandler())
app_logger.setLevel(logging.INFO)
app_logger.info("best")
print("---------------------------")

processed_image = None
initial_image = None
image_encoded = False
image_decoded = False

if 'original_filename' not in st.session_state:
    st.session_state.original_filename = None

tab1, tab2 = st.tabs(["Encode", "Decode"])

def preprocess_image(streamlit_opened_image):
    return np.array(Image.open(streamlit_opened_image))

with tab1:
    st.header("Encode section")
    with st.form("upload_form"):
        st.write("Upload an image here with a maximum file size of 200mb")

        image = st.file_uploader(label="Image upload", type =["jpg", "jpeg", "png"])
        
        #TODO: What is my image being read as and how is it being converted
        if image is not None:
            st.image(image)
            name = image.name
            app_logger.info(name)
            initial_image = np.array(Image.open(image))
            app_logger.info(initial_image)

        hidden_message = st.text_input(label="Add in your hidden message here")
        
        submitted = st.form_submit_button("Submit")

        if submitted: #and encoded image is not None
            if hidden_message and initial_image is not None:
                processed_image = encode_message(initial_image, hidden_message)
            st.write("Image uploaded and Message Encoded")
            image_encoded = True
        
    if image_encoded:
        st.download_button(
                label="Download processed image",
                data=image,
                file_name=name,
            )

with tab2:
    st.header("Decode section")
    with st.form("download_form"):
        st.write("Upload an image here with a maximum file size of 200mb")

        image_to_decode = st.file_uploader(label="Image upload", type =["jpg", "jpeg", "png"])

        submitted = st.form_submit_button("Submit")

        if image_to_decode is not None:
            app_logger.info(image_to_decode)
            image_to_decode = preprocess_image(image_to_decode) #update the image
            decoded_image =decode_message(image_to_decode)

        if submitted:
            st.write("Processing Image and Decoding Message")
            image_decoded = True
            st.write(f"Processed! Your resulting message is: {decoded_image}")

