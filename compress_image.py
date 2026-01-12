# compress_image.py

import streamlit as st
from PIL import Image
from io import BytesIO
import numpy as np
from utils import apply_pca, validate_image  # Make sure utils.py is in the same directory

def upload_image():
    st.title("📤 Upload Image for Compression")
    st.write("Welcome to the Image Compression page! Here, you can upload your image and compress it using Principal Component Analysis (PCA).")

    # Upload the image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        if validate_image(uploaded_image):
            st.image(uploaded_image, caption="Original Image", use_column_width=True)

            # Load the image
            img = Image.open(uploaded_image)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img_byte = BytesIO()
            img.save(img_byte, format='JPEG')
            img_byte.seek(0)
            st.session_state['image'] = img_byte.getvalue()

            # Calculate the maximum number of principal components
            img_array = np.array(img)
            max_components = min(img_array.shape[0], img_array.shape[1])  # Total pixels vs channels
            st.session_state['max_components'] = max_components

            # Slider for choosing number of components
            num_components = st.slider("Number of Principal Components", min_value=1, max_value=max_components, value=10)

            if st.button("Compress Image"):
                with st.spinner('Processing...'):
                    import time  # Import time for measuring compression duration
                    start_time = time.time()  # Start timer
 
                    compressed_image_bytes = apply_pca(img_array, num_components)
                    compressed_image = Image.open(compressed_image_bytes)

                    # Calculate time taken
                    end_time = time.time()
                    time_taken = end_time - start_time

                    # Display compressed image
                    st.image(compressed_image, caption="Compressed Image", use_column_width=True)

                    st.session_state['original_image'] = uploaded_image
                    st.session_state['compressed_image'] = compressed_image_bytes
                    st.session_state['no_of_components'] = num_components

                    # Display compression time and variance ratio
                    st.markdown(f"### Compression Time: {time_taken:.2f} seconds")
                    

                    # Save and download compressed image
                    st.markdown("### Save Compressed Image")
                    img_bytes = BytesIO()
                    compressed_image.save(img_bytes, format='JPEG')
                    img_bytes.seek(0)

                    download_btn = st.download_button(
                        label="Download Compressed Image",
                        data=img_bytes,
                        file_name="compressed_image.jpg",
                        mime="image/jpeg",
                        key="download_compressed_img"
                    )

        else:
            st.error("Unsupported file format. Please upload a jpg, jpeg, or png file.")
            
            # Display the next button
    if st.button("**How PCA works ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % 7
        st.rerun()