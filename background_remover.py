# background_remover.py

import streamlit as st
from PIL import Image
from rembg import remove
from io import BytesIO

def background_remover_page():
    st.title("🎭 Background Remover")
    
    # Add description
    st.markdown("""
    Remove the background from your images instantly! Upload an image and let our AI do the magic.
    
    **Supported formats:** PNG, JPG, JPEG
    """)

    # File uploader
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Display original image
        image = Image.open(uploaded_file)
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original Image")
            st.image(image, use_column_width=True)

        # Remove background
        if st.button("Remove Background"):
            with st.spinner("Processing..."):
                # Remove background
                output = remove(image)
                
                # Display result
                with col2:
                    st.subheader("Processed Image")
                    st.image(output, use_column_width=True)
                
                # Convert to bytes for download
                img_byte_arr = BytesIO()
                output.save(img_byte_arr, format='PNG')
                img_byte_arr.seek(0)
                
                # Download button
                st.download_button(
                    label="Download processed image",
                    data=img_byte_arr,
                    file_name="processed_image.png",
                    mime="image/png"
                )

    # Add helpful tips
    with st.expander("Tips for best results"):
        st.markdown("""
        - Use images with clear subjects
        - Ensure good lighting
        - Avoid very complex backgrounds
        - Higher resolution images work better
        """)

    # Add footer
    st.markdown("---")
    st.markdown("Background removal powered by rembg")

    # Navigation button
    if st.button("**Feedback ⇨**", key="next"):  # Changed key here
        st.session_state.page_index = (st.session_state.page_index + 1) % 7
        st.rerun()