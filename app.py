from matplotlib.path import Path
import streamlit as st
from PIL import Image
from io import BytesIO
from utils import apply_pca, validate_image #type:ignore
from streamlit_star_rating import st_star_rating
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
from pathlib import Path
import cv2
import io
from skimage.color import rgb2lab, lab2rgb
import requests
import datetime
import json
from rembg import remove

# Function to load images from URLs
def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

def load_image_from_path(image_path):
    img = Image.open(image_path)
    return img

# Set page config
st.set_page_config(
    page_title="PCA ImageXpert",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Streamlit navigation
def navigate_pages(pages):
    # Initialize the session state
    if 'page_index' not in st.session_state:
        st.session_state['page_index'] = 0

    # Set the radio button selection to the current page
    page = st.sidebar.radio("Select a page:", pages, index=st.session_state.page_index)

    # Return the current page
    return page

# Streamlit navigation
st.sidebar.header(" NAVIGATION", divider='rainbow')

pages = ["Home", "Compress Image", "How PCA Works", "Compare Images", "Learn PCA","Background Remover","Feedback"]

# Call the navigate_pages function and store the current page
current_page = navigate_pages(pages)

# Custom CSS for styling
st.markdown("""
    <style>
    .body {background-color: #f2c698;}
    .main {
            background-image: url("https://images.unsplash.com/photo-1528460033278-a6ba57020470?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTAyfHxtYWNoaW5lJTIwbGVhcm5pbmclMjBsaWdodCUyMGJhY2tncm91bmR8ZW58MHx8MHx8fDA%3D");
            background-size: cover;
#        background-color: #add8e0;
    }
    .appview-container .sidebar .sidebar-content {
            background-image: url("https://images.unsplash.com/photo-1528460033278-a6ba57020470?w=800&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTAyfHxtYWNoaW5lJTIwbGVhcm5pbmclMjBsaWdodCUyMGJhY2tncm91bmR8ZW58MHx8MHx8fDA%3D");
            background-size: cover;
#        background-color: #fff;
    }
    .sidebar .sidebar-header {
    }
    .stButton > button {
        background-color: #4CAFFE;
        color: aliceblue;
    }
    .stSlider > div {
        color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# Page functions
def home():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Merriweather:wght@700&display=swap'); /* Importing Merriweather from Google Fonts */

        .art-title {
            font-family: 'Merriweather', serif; /* Professional and beautiful font */
            text-align: center;
            color: #2c3e50; /* Dark blue color for the text */
            text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.5), 6px 6px 10px rgba(0, 0, 0, 0.3); /* Enhanced shadows for 3D effect */
            font-size: 53px; /* Adjusted font size for professionalism */
            margin: 20px 0; /* Reduced margin */
            letter-spacing: 2px;
            line-height: 1.0;
        }
        body {
            background-color: #FFFFFF; /* White background */
            color: #000000; /* Black text color */
        }
    </style>
    <h1 class="art-title">
    📸 PCA ImageXpert 
    </h1>
    """, unsafe_allow_html=True)


    st.markdown("""
        <style>
        .big-paragraph {
            font-size: 20px;
            line-height: 1.5;
            margin-top: 20px;
            text-align: left;
            }
            .sub {
                font-family: 'Merriweather', serif; /* Professional and beautiful font */
                text-align: center;
                font-size: 23px;
                font-weight: bold; /* Making the text bold */
                margin: 2px 0; /* Adding margin */
                line-height: 1.5; /* Adjusting line height */
                letter-spacing: 1.3px; /* Adjusting letter spacing */
            }
            @keyframes moveLeft {
            0% { transform: translateX(0px); }
            50% { transform: translateX(-10px); }
            100% { transform: translateX(0px); }
            }

            .moving-emoji-container {
            display: flex;
            justify-content: center;
            }

            .moving-emoji {
            animation: moveLeft 1s infinite;
            font-size: 39px; /* Adjust the size as needed */
            }
        </style>
        <p class="sub">Welcome to PCA ImageXpert!</p>
        <p class="big-paragraph">
        Unlock the power of Principal Component Analysis (PCA) with PCA ImageXpert, your comprehensive, pedagogical platform designed to make learning and applying PCA accessible, engaging, and fun. Whether you’re a tech nerd diving deep into the logic and code, or a beginner exploring the basics, PCA ImageXpert is crafted to guide you through the fascinating world of unsupervised machine learning with ease.
        <p><strong style="font-size: 24px;">Navigate Your PCA Journey</strong>.</p>
        <!-- Example of including image using HTML in a single line with options for changing size and alignment -->
        <img src="https://www.designnominees.com/application/blog-images/website-easy-to-navigate.png" alt="Image" style="width: 600px; height: auto; margin: auto; display: block;">
        <br>
            <p style="font-size: 20px;">Our intuitive navigation bar helps you explore all the features PCA ImageXpert offers:</p>
            <p><strong style="font-size: 20px;">Home:</strong> <span style="font-size: 20px;">Return to the main page anytime to see the latest updates and featured content.</span></p>
            <p><strong style="font-size: 20px;">Compress Image:</strong> <span style="font-size: 20px;">Effortlessly upload your images in JPG, JPEG, or PNG format and experience the magic of PCA-powered image compression. Other formats are not supported to ensure the best quality and performance.</span></p>
            <p><strong style="font-size: 20px;">How PCA works:</strong> <span style="font-size: 20px;">Dive into the detailed workings of PCA. Understand the underlying logic, algorithms, and code implementations. Perfect for those who want to get into the technical nitty-gritty.</span></p>
            <p><strong style="font-size: 20px;">Learn PCA:</strong> <span style="font-size: 20px;">Start from scratch with our beginner-friendly tutorials. We break down complex concepts into easy-to-understand lessons, making PCA accessible even to a child.</span></p>
            <p><strong style="font-size: 20px;">Compare Images:</strong> <span style="font-size: 20px;">See the difference PCA makes. Upload an image, let our application compress it, and then compare the original and compressed versions side by side. Analyze various metrics and view histograms of the similarity index to understand the effectiveness of the compression.</span></p>
            <p><strong style="font-size: 20px;">Feedback:</strong> <span style="font-size: 20px;">Share your thoughts and see what others have to say. Your feedback helps us improve, and we value every suggestion.</span></p>
            <p><strong style="font-size: 20px;">View Feedback:</strong><span style="font-size: 20px;"> This feature allows users to see feedbacks and suggestions given by users.</span></p>
            <p><strong style="font-size: 24px;">Why PCA ImageXpert?</strong></p>
        <img src="https://plannersweb.com/wp-content/uploads/1993/01/why-word.jpg" alt="Image" style="width: 500px; height: auto; margin: auto; display: block;">
        <br>
            <p style="font-size: 20px;">PCA ImageXpert isn’t just another tech tool; it’s a learning companion. We believe in honesty, clarity, and making complex subjects approachable. Our features are designed to provide a seamless experience, whether you’re learning the basics or exploring advanced applications.</p>
            <p style="font-size: 20px;"><strong>Educational:</strong> Learn PCA in a structured, easy-to-follow way.</p>
            <p style="font-size: 20px;"><strong>Practical:</strong> Apply PCA to real-world tasks like image compression.</p>
            <p style="font-size: 20px;"><strong>Interactive:</strong> Compare and analyze results to deepen your understanding.</p>
            <p style="font-size: 20px;"><strong>Community-Driven:</strong> Engage with a community of learners and tech enthusiasts through feedback and shared experiences.</p>
            <p style="font-size: 20px;">Join us on PCA ImageXpert and transform your understanding of PCA from theory to practice. Let’s make data science not just understandable but also enjoyable for everyone.</p>
            <p style="font-size: 20px;">Welcome aboard, and happy learning!</p>
            <p style="font-size: 20px;">By using our application, you can see these principles in action and understand the impact of PCA on image processing. Start with the Compress Image feature to see how much space you can save without losing significant details.</p>
        </p>
        
        <div class="moving-emoji-container">
        <div class="moving-emoji">👈</div>
        </div>
    
    """, unsafe_allow_html=True)
    
    st.markdown("""
    For more information, visit our [documentation](https://example.com/documentation) or contact our [support team](https://example.com/support).
    """)

    st.markdown("""
        <footer style="position: fixed; bottom: 0; left: 0; width: 100%; margin: 0; text-align: center; font-size: 14px; color: black; border: 1px solid #333; color: #fff; background-color: black">
        @All rights reserved. Quantum Inno Vissionaries
        </footer>
                """, unsafe_allow_html=True)
    
    # Display the next button
    if st.button("**Compress Image ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % len(pages)
        st.rerun()

def upload_image():
    st.title("📤 Upload Image")
    st.write("Upload your image here:")

    # Upload the image
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        if validate_image(uploaded_image):
            st.image(uploaded_image, caption="Original Image", use_column_width=True)

            # Load the image
            img = Image.open(uploaded_image)
            img_byte = BytesIO()
            img.save(img_byte, format='JPEG')
            img_byte.seek(0)
            st.session_state['image'] = img_byte.getvalue()

            # Calculate the maximum number of principal components
            img_array = np.array(img)
            max_components = min(img_array.shape[0], img_array.shape[1])
            st.session_state['max_components'] = max_components

            # Slider for choosing number of components
            num_components = st.slider("Number of Principal Components", min_value=1, max_value=500, value=10)

            if st.button("Compress Image"):
                with st.spinner('Processing...'):
                    # Compress the image using PCA
                    compressed_image_bytes = apply_pca(img, num_components)
                    compressed_image = Image.open(compressed_image_bytes)

                    # Display compressed image
                    st.image(compressed_image, caption="Compressed Image", use_column_width=True)

                    st.session_state['original_image'] = uploaded_image
                    st.session_state['compressed_image'] = compressed_image_bytes
                    st.session_state['no_of_components'] = num_components

                    # Save and download compressed image
                    st.markdown("### Save Compressed Image")
                    st.write("Click the button below to save and download the compressed image.")

                    # Convert PIL Image to bytes
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
    if st.button("**How PCA works!! ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % len(pages)
        st.rerun()

def how_pca_works():

    # Title and explanation of PCA
    st.title("📊 How PCA Works (For Technerds!)")

    show_pca_workings = st.checkbox("Show detailed workings of PCA")

    with st.container(border=True):
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
            if 'image' not in st.session_state:
                st.error("Please upload an image to see the detailed workings of PCA.")
                return
            original_image = Image.open(BytesIO(st.session_state['image']))
            no_of_components = st.session_state['no_of_components']

            # Function to apply PCA on an image
            def apply_pca(original_image, no_of_components):

                # Retrieve the number of components from the session state
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

            # Function to perform PCA compression on a single channel
            def pca_compress(channel, no_of_components, channel_name):
                # Subtract the mean from the data
                mean = np.mean(channel, axis=0)
                centered_data = channel - mean

                # Normalize centered data for display
                centered_display_data = (centered_data - np.min(centered_data)) / (np.max(centered_data) - np.min(centered_data))
                #st.image(centered_display_data, caption=f'Step in {channel_name}: Centered Data', use_column_width=True)

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
                #st.image(compressed_display_data, caption=f'Step in {channel_name}: Compressed Data', use_column_width=True)

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

    # Display the next button
    if st.button("**Compare Images ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % len(pages)
        st.rerun()

def display_metrics(original_file, compressed_image):
    # Get the size of the original uploaded file
    original_size = original_file.size

    # Ensure the compressed image is read from BytesIO if necessary
    if isinstance(compressed_image, BytesIO):
        compressed_image = Image.open(compressed_image)

    compressed_bytes = BytesIO()
    compressed_image.save(compressed_bytes, format='JPEG')
    compressed_size = len(compressed_bytes.getvalue())

    compression_ratio = original_size / compressed_size

    st.write(f"**Original Size:** {original_size / 1024:.2f} KB")
    st.write(f"**Compressed Size:** {compressed_size / 1024:.2f} KB")
    st.write(f"**Compression Ratio:** {compression_ratio:.2f}")

    original_array = np.array(Image.open(original_file))
    compressed_array = np.array(compressed_image)

    # Compute SSIM with explicit window size and channel axis
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

def display_pixel_intensity_comparison(original_image, compressed_image):
    original_array = np.array(original_image.convert("L"))
    compressed_array = np.array(compressed_image.convert("L"))

    fig, ax = plt.subplots()
    ax.hist(original_array.ravel(), bins=256, color='blue', alpha=0.5, label='Original')
    ax.hist(compressed_array.ravel(), bins=256, color='orange', alpha=0.5, label='Compressed')
    ax.set_title('Pixel Intensity Distribution Comparison')
    ax.set_xlabel('Pixel Intensity')
    ax.set_ylabel('Frequency')
    ax.legend()
    st.pyplot(fig)

def display_color_channel_comparison(original_image, compressed_image):
    original_array = np.array(original_image)
    compressed_array = np.array(compressed_image)

    fig, axs = plt.subplots(2, 3, figsize=(15, 10))

    for i, color in enumerate(['Red', 'Green', 'Blue']):
        axs[0, i].hist(original_array[:, :, i].ravel(), bins=256, color=color.lower(), alpha=0.5)
        axs[0, i].set_title(f'Original {color} Channel Histogram')

        axs[1, i].hist(compressed_array[:, :, i].ravel(), bins=256, color=color.lower(), alpha=0.5)
        axs[1, i].set_title(f'Compressed {color} Channel Histogram')

    st.pyplot(fig)

def display_edge_detection_comparison(original_image, compressed_image):
    from skimage.filters import sobel

    original_gray = np.array(original_image.convert("L"))
    compressed_gray = np.array(compressed_image.convert("L"))

    original_edges = sobel(original_gray)
    compressed_edges = sobel(compressed_gray)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    ax1.imshow(original_edges, cmap='gray')
    ax1.set_title('Original Image Edges')

    ax2.imshow(compressed_edges, cmap='gray')
    ax2.set_title('Compressed Image Edges')

    st.pyplot(fig)

def display_ssim_map(original_image, compressed_image):
    from skimage.metrics import structural_similarity as ssim

    original_array = np.array(original_image.convert("L"))
    compressed_array = np.array(compressed_image.convert("L"))

    ssim_index, ssim_image = ssim(original_array, compressed_array, full=True)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(ssim_image, cmap='gray')
    ax.set_title(f'SSIM Map (Score: {ssim_index:.4f})')
    st.pyplot(fig)

def display_color_distribution(original, compressed):
    def plot_color_distribution(image, title):
        image_array = np.array(image)
        pixels = image_array.reshape(-1, 3)
        
        fig = plt.figure(figsize=(5, 3))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(pixels[:, 0], pixels[:, 1], pixels[:, 2], c=pixels/255, s=1)
        ax.set_title(title)
        ax.set_xlabel('Red')
        ax.set_ylabel('Green')
        ax.set_zlabel('Blue')
        st.pyplot(fig)
    
    col1, col2 = st.columns(2)
    
    with col1:
        plot_color_distribution(original, "Original Color Distribution")
    
    with col2:
        plot_color_distribution(compressed, "Compressed Color Distribution")
        
def display_frequency_domain_analysis(original, compressed):
    def fft_image(image):
        image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        f_transform = np.fft.fft2(image_gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude_spectrum = 20 * np.log(np.abs(f_shift))
        return magnitude_spectrum
    
    original_fft = fft_image(original)
    compressed_fft = fft_image(compressed)
    
    col1, col2 = st.columns(2)
    
    with col1:
        plt.figure(figsize=(5, 3))
        plt.imshow(original_fft, cmap='gray')
        plt.title("Original Image Frequency Domain")
        plt.axis('off')
        st.pyplot(plt)
    
    with col2:
        plt.figure(figsize=(5, 3))
        plt.imshow(compressed_fft, cmap='gray')
        plt.title("Compressed Image Frequency Domain")
        plt.axis('off')
        st.pyplot(plt)

def display_contour_plots(original, compressed):
    def contour_plot(image, title):
        image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        plt.figure(figsize=(5, 3))
        plt.contour(image_gray, cmap='viridis')
        plt.title(title)
        plt.axis('off')
        st.pyplot(plt)
    
    col1, col2 = st.columns(2)
    
    with col1:
        contour_plot(original, "Original Image Contours")
    
    with col2:
        contour_plot(compressed, "Compressed Image Contours")

def display_color_difference_maps(original, compressed):
    original_lab = rgb2lab(np.array(original))
    compressed_lab = rgb2lab(np.array(compressed))
    
    diff_lab = np.abs(original_lab - compressed_lab)
    diff_l = diff_lab[:, :, 0]
    diff_a = diff_lab[:, :, 1]
    diff_b = diff_lab[:, :, 2]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        plt.figure(figsize=(5, 3))
        plt.imshow(diff_l, cmap='gray')
        plt.colorbar()
        plt.title("L* Difference")
        plt.axis('off')
        st.pyplot(plt)
    
    with col2:
        plt.figure(figsize=(5, 3))
        plt.imshow(diff_a, cmap='gray')
        plt.colorbar()
        plt.title("a* Difference")
        plt.axis('off')
        st.pyplot(plt)
    
    with col3:
        plt.figure(figsize=(5, 3))
        plt.imshow(diff_b, cmap='gray')
        plt.colorbar()
        plt.title("b* Difference")
        plt.axis('off')
        st.pyplot(plt)

def display_sharpness_comparison(original, compressed):
    def image_sharpness(image):
        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
        sharpness = np.var(laplacian)
        return sharpness
    
    original_sharpness = image_sharpness(original)
    compressed_sharpness = image_sharpness(compressed)
    
    st.write(f"**Original Image Sharpness**: {original_sharpness:.2f}")
    st.write(f"**Compressed Image Sharpness**: {compressed_sharpness:.2f}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Original Image**")
        st.image(original, caption=f"Sharpness: {original_sharpness:.2f}", use_column_width=True)
    
    with col2:
        st.write("**Compressed Image**")
        st.image(compressed, caption=f"Sharpness: {compressed_sharpness:.2f}", use_column_width=True)

def comparison():
    st.title("🖼️ Compare Images")
    
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
        display_metrics(st.session_state['original_image'], st.session_state['compressed_image'])
        
        st.subheader("Histograms")
        col3, col4 = st.columns(2)
        
        with col3:
            display_histogram(original_image, "Original Image Histogram")
        
        with col4:
            display_histogram(compressed_image, "Compressed Image Histogram")
        
        st.subheader("Additional Analyses")
        
        st.write("### Pixel Intensity Comparison")
        display_pixel_intensity_comparison(original_image, compressed_image)
        
        st.write("### Color Channel Comparison")
        display_color_channel_comparison(original_image, compressed_image)
        
        st.write("### Edge Detection Comparison")
        display_edge_detection_comparison(original_image, compressed_image)
        
        st.write("### SSIM Map")
        display_ssim_map(original_image, compressed_image)
        
        st.write("### Color Distribution")
        display_color_distribution(original_image, compressed_image)
        
        st.write("### Frequency Domain Analysis")
        display_frequency_domain_analysis(original_image, compressed_image)
        
        st.write("### Contour Plots")
        display_contour_plots(original_image, compressed_image)
        
        st.write("### Color Difference Maps")
        display_color_difference_maps(original_image, compressed_image)
        
        st.write("### Sharpness Comparison")
        display_sharpness_comparison(original_image, compressed_image)
    else:
        st.write("No images stored for comparison.")

        
    # Display the next button
    if st.button("**Learn PCA ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % len(pages)
        st.rerun()
        

def load_feedback(file_path):
    if Path(file_path).exists():
        with open(file_path, 'r') as f:
            return json.load(f)
    return []

def save_feedback(file_path, feedback_data):
    with open(file_path, 'w') as f:
        json.dump(feedback_data, f, indent=4)

def feedback():
    st.title("💬 Feedback")
    st.write("Please provide your feedback and suggestions here.")
    
    st.subheader("Rating:")
    stars = st_star_rating(label="Please rate your experience", maxValue=5, defaultValue=0, key="rating", resetLabel="Reset", customCSS="div {background-color: white;}")
    
    st.subheader("Feedback Comment:")
    feedback_comment = st.text_area("Please leave your feedback comment here.")
    
    if st.button("Submit"):
        if stars and feedback_comment:
            feedback_data = {
                "rating": stars,
                "comment": feedback_comment,
                "timestamp": datetime.datetime.now().isoformat()
            }
            file_path = 'feedback.json'
            feedbacks = load_feedback(file_path)
            feedbacks.insert(0, feedback_data)  # Insert at the beginning
            save_feedback(file_path, feedbacks)
            st.success("Thank you for your feedback!")
        else:
            st.error("Please provide both rating and comment.")

    st.subheader("Previous Feedback:")
    feedbacks = load_feedback('feedback.json')
    for feedback in feedbacks:
        st.write(f"Rating: {feedback['rating']} stars")
        st.write(f"Comment: {feedback['comment']}")
        st.write(f"Submitted on: {feedback['timestamp']}")
        st.write("---")

    # Display the next button
    if st.button("**Return to Home Page ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % len(pages)
        st.rerun()

def load_pca_content():
    with open("pca_content.json", "r") as file:
        content = json.load(file)
    return content

def what_PCA():
    st.title("Learn PCA")
    content = load_pca_content()
    tutorials = content['tutorials']
    quizzes = content['quizzes']
    faqs = content['faqs']
    
    if 'tutorial_index' not in st.session_state:
        st.session_state.tutorial_index = 0
    if 'quiz_index' not in st.session_state:
        st.session_state.quiz_index = 0 
        

    def display_tutorial(index):
        tutorial = tutorials[index]
        st.subheader(tutorial['title'])
        st.markdown(tutorial['content'])
        for eq in tutorial['equations']:
            st.latex(eq['latex'])
        if 'image' in tutorial:
            st.image(tutorial['image'], width=500)

    def next_tutorial():
        if st.session_state.tutorial_index < len(tutorials) - 1:
            st.session_state.tutorial_index += 1
        st.session_state.quiz_index = 0
        st.session_state.quiz_answer = 0
        st.experimental_rerun()

    def display_quiz(index):
        quiz = quizzes[index]
        st.subheader("Quiz")
        st.write(quiz['question'])
        options = quiz['options']
        selected_option = st.radio("Choose an option", options, key=f"quiz_{index}")
        if st.button("Submit Answer", key=f"submit_{index}"):
            st.session_state.quiz_answer = selected_option
            if selected_option == quiz['answer']:
                st.success("Correct!")
            else:
                st.error("Incorrect. The correct answer is: " + quiz['answer'])
                st.stop()  # Stop execution to prevent access to the next tutorial

    display_tutorial(st.session_state.tutorial_index)

    if st.session_state.quiz_answer is None:
        display_quiz(st.session_state.quiz_index)
    elif st.session_state.quiz_index < 2:  # Limit to 3 quizzes per tutorial
        st.session_state.quiz_index += 1
        st.session_state.quiz_answer = None
        st.experimental_rerun()
    elif st.session_state.tutorial_index < len(tutorials) - 1:
        if st.button("Next Tutorial"):
            next_tutorial()

    st.subheader("FAQs")
    for faq in faqs:
        st.markdown(f"**{faq['question']}**")
        st.markdown(f"{faq['answer']}")

    # Display the next button
    if st.button("**Feedback ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % len(pages)
        st.rerun()
    

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


if current_page == "Home":
    home()
elif current_page == "Compress Image":
    upload_image()
elif current_page == "How PCA Works":
    how_pca_works()
elif current_page == "Compare Images":
    comparison()
elif current_page == "Learn PCA":
    what_PCA()
elif current_page == "Background Remover":
    Background_rem()
elif current_page == "Feedback":
    feedback()


def generate_footer():
    return """
    <footer style="text-align: center; font-size: 14px; color: black;">
        This is the footer text. You can add any additional information or links here.
    </footer>
    """
