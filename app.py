import streamlit as st
from PIL import Image
from io import BytesIO
from utils import apply_pca, validate_image
import base64
from streamlit_star_rating import st_star_rating
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import requests

# Function to load images from URLs
def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

# Set page config
st.set_page_config(
    page_title="Image PCA - Do & Learn",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background-color: #fff;
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
    }
    .stSlider > div {
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# Page functions
def home():
    st.title("📸 Image PCA - Do & Learn")
    st.markdown("""
        Welcome to **Image PCA - Do & Learn**!
        - Upload your images to compress and learn about PCA.
        - Navigate through the sidebar to explore different features.
    """)

    # Load and display images to demonstrate PCA applications
    images_urls = [
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRBsA0XGxXRQzuNJ5uVgfqLXaJWtlsUfOaW6P9NMaMDcw&s",
        "https://i.ytimg.com/vi/wCtLgEZd0Gw/maxresdefault.jpg",
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5a4mZ1KMH67p7OgE4zzyhIyMaaDjRQru74w&s"
    ]

    st.image(load_image(images_urls[0]), caption='PCA for Image Compression', use_column_width=True)
    st.image(load_image(images_urls[1]), caption='Comparison Before and After PCA', use_column_width=True)
    st.image(load_image(images_urls[2]), caption='Understanding PCA', use_column_width=True)

    st.markdown("""
    ## Features
    Explore the different features of our application:
    - **[Home](#home-page)**
    - **[Compress Image](#compress-image)**
    - **[Comparison](#comparison)**
    - **[How PCA Works for Technerds](#how-pca-works-for-technerds)**
    - **[What is PCA](#what-is-pca)**
    - **[Feedback](#feedback)**
    - **[View Feedback](#view-feedback)**

    ## Know More
    To dive deeper into PCA and its applications, click on the tabs above and start exploring!
    """)

    st.markdown("""
    ### Why PCA?
    Principal Component Analysis (PCA) is a powerful statistical technique used for dimensionality reduction. It's widely used in:
    - **Image Compression:** Reducing the size of images while preserving essential features.
    - **Noise Reduction:** Enhancing image quality by removing noise.
    - **Feature Extraction:** Identifying important features in large datasets, often used in machine learning models.

    By using our application, you can see these principles in action and understand the impact of PCA on image processing. Start with the **Compress Image** feature to see how much space you can save without losing significant details.
    """)

    st.markdown("""
    For more information, visit our [documentation](https://example.com/documentation) or contact our [support team](https://example.com/support).
    """)

def upload_image():
    st.title("📤 Compress Image")
    st.write("Upload your image here:")

    # Upload the image
    uploaded_image= st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_image:
        if validate_image(uploaded_image):
            st.image(uploaded_image, caption="Original Image", use_column_width=True)
            
            # Load the image
            img = Image.open(uploaded_image)
        
            
            # Slider for choosing number of components
            num_components = st.slider("Number of Principal Components", min_value=1, max_value=500, value=10)

            if st.button("Compress Image"):
                # Compress the image using PCA
                compressed_image_bytes = apply_pca(img, num_components)
                compressed_image = Image.open(compressed_image_bytes)
                
                # Display compressed image
                st.image(compressed_image, caption="Compressed Image", use_column_width=True)
                
                
                st.session_state['original_image'] = uploaded_image
                st.session_state['compressed_image'] = compressed_image_bytes
                st.session_state['no_of_components'] = num_components
                
                
                # Save and download compressed image
                st.write("Click the button below to save and download the compressed image.")
                
                # Convert PIL Image to bytes
                img_bytes = BytesIO()
                compressed_image.save(img_bytes, format='JPEG')
                img_bytes.seek(0)
                st.session_state['image'] = img_bytes.getvalue()
                
                download_btn = st.download_button(
                    label="Download Compressed Image", 
                    data=img_bytes, 
                    file_name="compressed_image.jpg", 
                    mime="image/jpeg", 
                    key="download_compressed_img"
                )
                
        else:
            st.error("Unsupported file format. Please upload a jpg, jpeg, or png file.")

def how_pca_works():
    # Title and explanation of PCA
    st.title("📊 How PCA Works (For Technerds)")
    
    show_pca_workings = st.checkbox("Show detailed workings of PCA")

    if show_pca_workings:
        st.markdown("""
            ### Detailed Workings of PCA:
            
            1. **Convert image to numpy array**:
            ```python
            img_array = np.array(img)
            ```
            
            2. **Splitting RGB channels**:
            ```python
            red_channel = img_array[:, :, 0]
            green_channel = img_array[:, :, 1]
            blue_channel = img_array[:, :, 2]
            ```
            
            3. **Apply PCA on each channel**:
            ```python
            red_compressed = pca_compress(red_channel, num_components)
            green_compressed = pca_compress(green_channel, num_components)
            blue_compressed = pca_compress(blue_channel, num_components)
            ```
            
            4. **Combine compressed channels into one image**:
            ```python
            compressed_img_array = np.stack((red_compressed, green_compressed, blue_compressed), axis=2)
            compressed_img = Image.fromarray(np.uint8(compressed_img_array))
            ```
            
            5. **Function to perform PCA compression on a single channel**:
            ```python
            def pca_compress(channel, num_components):
                # Subtract the mean from the data
                mean = np.mean(channel, axis=0)
                centered_data = channel - mean

                # Compute the covariance matrix
                cov_matrix = np.cov(centered_data, rowvar=False)

                # Compute the eigenvalues and eigenvectors of the covariance matrix
                eig_vals, eig_vecs = np.linalg.eigh(cov_matrix)

                # Sort eigenvalues and eigenvectors in descending order
                sorted_indices = np.argsort(eig_vals)[::-1]
                sorted_eig_vals = eig_vals[sorted_indices]
                sorted_eig_vecs = eig_vecs[:, sorted_indices]

                # Choose the number of principal components
                if num_components > len(sorted_eig_vals):
                    num_components = len(sorted_eig_vals)
                elif num_components < 1:
                    num_components = 1

                # Project the data onto the selected principal components
                projection_matrix = sorted_eig_vecs[:, :num_components]
                compressed_data = np.dot(centered_data, projection_matrix)

                # Reconstruct the data
                reconstructed_data = np.dot(compressed_data, projection_matrix.T) + mean

                # Clip the values to [0, 255]
                reconstructed_data = np.clip(reconstructed_data, 0, 255)

                return reconstructed_data.astype(np.uint8)
            ```
        """)

        original_image = Image.open(BytesIO(st.session_state['image']))
        no_of_components = st.session_state['no_of_components']
        
        def apply_pca(original_image, no_of_components):
            img_array = np.array(original_image.convert("RGB"))
            st.image(img_array, caption='Original Image', use_column_width=True)
            
            # Splitting RGB channels
            red_channel = img_array[:, :, 0]
            green_channel = img_array[:, :, 1]
            blue_channel = img_array[:, :, 2]
            
            st.image(red_channel, caption='Step 2: Red Channel', use_column_width=True)
            st.image(green_channel, caption='Step 2: Green Channel', use_column_width=True)
            st.image(blue_channel, caption='Step 2: Blue Channel', use_column_width=True)

            # Apply PCA on each channel
            red_compressed = pca_compress(red_channel, no_of_components , 'Red Channel')
            green_compressed = pca_compress(green_channel, no_of_components , 'Green Channel')
            blue_compressed = pca_compress(blue_channel, no_of_components , 'Blue Channel')

            # Combine compressed channels into one image
            compressed_img_array = np.stack((red_compressed, green_compressed, blue_compressed), axis=2)
            compressed_img = Image.fromarray(np.uint8(compressed_img_array))
            st.image(compressed_img, caption='Compressed Image', use_column_width=True)

            # Convert compressed image to BytesIO for storage
            compressed_img_bytes = BytesIO()
            compressed_img.save(compressed_img_bytes, format='JPEG')
            compressed_img_bytes.seek(0)
            return compressed_img_bytes

        def pca_compress(channel, no_of_components, channel_name):
            # Subtract the mean from the data
            mean = np.mean(channel, axis=0)
            centered_data = channel - mean
            
            # Normalize centered data for display
            centered_display_data = (centered_data - np.min(centered_data)) / (np.max(centered_data) - np.min(centered_data))
            
            # Compute the covariance matrix
            cov_matrix = np.cov(centered_data, rowvar=False)
            st.text(f'Step in {channel_name}: Covariance Matrix\n{cov_matrix}')

            # Compute the eigenvalues and eigenvectors of the covariance matrix
            eig_vals, eig_vecs = np.linalg.eigh(cov_matrix)

            # Sort eigenvalues and eigenvectors in descending order
            sorted_indices = np.argsort(eig_vals)[::-1]
            sorted_eig_vals = eig_vals[sorted_indices]
            sorted_eig_vecs = eig_vecs[:, sorted_indices]

            # Show sorted eigenvalues and eigenvectors
            st.text(f'Step in {channel_name}: Sorted Eigenvalues\n{sorted_eig_vals}')
            st.text(f'Step in {channel_name}: Sorted Eigenvectors\n{sorted_eig_vecs}')

            # Choose the number of principal components
            if no_of_components > len(sorted_eig_vals):
                no_of_components = len(sorted_eig_vals)
            elif no_of_components < 1:
                no_of_components = 1

            # Project the data onto the selected principal components
            projection_matrix = sorted_eig_vecs[:, :no_of_components]
            compressed_data = np.dot(centered_data, projection_matrix)
            
            # Normalize compressed data for display
            compressed_display_data = (compressed_data - np.min(compressed_data)) / (np.max(compressed_data) - np.min(compressed_data))

            # Reconstruct the data
            reconstructed_data = np.dot(compressed_data, projection_matrix.T) + mean
            
            # Normalize reconstructed data for display
            reconstructed_display_data = (reconstructed_data - np.min(reconstructed_data)) / (np.max(reconstructed_data) - np.min(reconstructed_data))
            st.image(reconstructed_display_data, caption=f'Step in {channel_name}: Reconstructed Data', use_column_width=True)

            # Clip the values to [0, 255] for the final output
            reconstructed_data = np.clip(reconstructed_data, 0, 255)

            return reconstructed_data.astype(np.uint8)
        
        if st.button('Apply PCA'):
            apply_pca(original_image, no_of_components)

def display_metrics(original_image, compressed_image):
    original_bytes = BytesIO()
    compressed_bytes = BytesIO()

    original_image.save(original_bytes, format='JPEG')
    compressed_image.save(compressed_bytes, format='JPEG')

    original_size = len(original_bytes.getvalue())
    compressed_size = len(compressed_bytes.getvalue())

    compression_ratio = original_size / compressed_size

    st.write(f"**Original Size:** {original_size / 1024:.2f} KB")
    st.write(f"**Compressed Size:** {compressed_size / 1024:.2f} KB")
    st.write(f"**Compression Ratio:** {compression_ratio:.2f}")

    original_array = np.array(original_image)
    compressed_array = np.array(compressed_image)

    win_size = min(original_array.shape[0], original_array.shape[1], compressed_array.shape[0], compressed_array.shape[1], 7)
    ssim_index = ssim(original_array, compressed_array, win_size=win_size, channel_axis=-1)
    
    st.write(f"**SSIM (Structural Similarity Index):** {ssim_index:.4f}")

def display_histogram(image, title):
    img_array = np.array(image)
    fig, ax = plt.subplots()
    ax.hist(img_array.ravel(), bins=256, color='orange', alpha=0.5)
    ax.set_title(title)
    ax.set_xlabel('Pixel Intensity')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

def comparison():
    st.title("🖼️ Stored Images")
    
    if 'original_image' in st.session_state and 'compressed_image' in st.session_state:
        st.subheader("Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            original_image = Image.open(st.session_state['original_image'])
            st.image(original_image, caption="Original Image", use_column_width=True)
        
        with col2:
            compressed_image = Image.open(st.session_state['compressed_image'])
            st.image(compressed_image, caption="Compressed Image", use_column_width=True)
        
        st.subheader("Metrics")
        display_metrics(original_image, compressed_image)
        
        st.subheader("Histograms")
        col3, col4 = st.columns(2)
        
        with col3:
            display_histogram(original_image, "Original Image Histogram")
        
        with col4:
            display_histogram(compressed_image, "Compressed Image Histogram")
            
    else:
        st.write("**Warning**: Upload the Image first!")

def init_session():
    return {"feedback_data": []}

session_state = st.session_state

if "feedback_data" not in session_state:
    session_state.update(init_session())

def feedback():
    st.title("💬 Feedback")
    st.write("Please provide your feedback and suggestions here.")
    
    st.subheader("Rating:")
    stars = st_star_rating(label="Please rate your experience", maxValue=5, defaultValue=0, key="rating", resetLabel="Reset", customCSS="div {background-color: white;}")
    st.write(stars)

    st.subheader("Feedback Comment:")
    feedback_comment = st.text_area("Please leave your feedback comment here.")
    
    if st.button("Submit Feedback"):
        session_state.feedback_data.append({"feedback": feedback_comment, "rating": stars})
        st.success("Thank you for your feedback!")

def view_Feedback():
    st.title("View Feedback")
    st.write("Here are the feedback and suggestions provided by users:")

    feedback_data = session_state.feedback_data

    if feedback_data:
        for index, feedback_entry in enumerate(feedback_data, start=1):
            st.subheader(f"Feedback #{index}")
            st.write(f"Rating: {feedback_entry['rating']}")
            st.write(f"Feedback: {feedback_entry['feedback']}")
            st.markdown("---")
    else:
        st.write("No feedback has been submitted yet.")

def what_PCA():
    st.title("But What is PCA?")
    st.markdown("""
    Principal Component Analysis (PCA) is a dimensionality-reduction method used to reduce the dimensionality of large data sets by transforming them into a new set of variables called principal components. These principal components are linear combinations of the original variables and are uncorrelated with each other.
    
    ### Key Concepts:
    - **Dimensionality Reduction:** PCA helps in reducing the number of variables while retaining most of the original variance.
    - **Principal Components:** New variables that are linear combinations of the original variables.
    - **Variance:** The measure of how much information is retained from the original dataset.

    ### Steps Involved:
    1. **Standardize the data.**
    2. **Compute the covariance matrix.**
    3. **Calculate the eigenvalues and eigenvectors.**
    4. **Sort the eigenvalues and select the top principal components.**
    5. **Transform the data into the new subspace.**

    PCA is widely used in fields such as image processing, data compression, and machine learning.
    """)

st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", ["Home", "Compress Image", "How PCA Works (For Technerds)", "Comparison", "But What is PCA?", "Feedback", "View Feedback"])

if page == "Home":
    home()
elif page == "Compress Image":
    upload_image()
elif page == "How PCA Works (For Technerds)":
    how_pca_works()
elif page == "Comparison":
    comparison()
elif page == "But What is PCA?":
    what_PCA()
elif page == "Feedback":
    feedback()
elif page == "View Feedback":
    view_Feedback()
