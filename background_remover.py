import io
import streamlit as st
from PIL import Image
from rembg import remove

def Background_rem():
    st.title("🌟 Background Remover")

    if 'original_image' not in st.session_state:
        st.session_state['original_image'] = None
    if 'processed_image' not in st.session_state:
        st.session_state['processed_image'] = None

    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.session_state['original_image'] = image
        st.image(image, caption='Uploaded Image', use_column_width=True)

    if st.session_state['original_image'] is not None:
        if st.button("Remove Background"):
            with st.spinner('Processing...'):
                image = st.session_state['original_image']
                # Convert PIL image to byte array
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                byte_im = buf.getvalue()
                # Remove background
                result = remove(byte_im)
                # Convert result byte array back to PIL image
                st.session_state['processed_image'] = Image.open(io.BytesIO(result))

    if st.session_state['processed_image'] is not None:
        st.image(st.session_state['processed_image'], caption='Background Removed', use_column_width=True)
        buf = io.BytesIO()
        st.session_state['processed_image'].save(buf, format="PNG")
        byte_im = buf.getvalue()
        st.download_button(
            label="Download Image",
            data=byte_im,
            file_name="background_removed.png",
            mime="image/png"
        )
        
    # Display the next button
    if st.button("**Feedback ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % len(pages)
        st.rerun()