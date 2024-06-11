from matplotlib.path import Path
import streamlit as st
from PIL import Image
from io import BytesIO
from utils import apply_pca, validate_image #type:ignore
import base64
from streamlit_star_rating import st_star_rating
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
from pathlib import Path
import requests
import datetime
import json

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

pages = ["Home", "Compress Image", "How PCA Works (For Technerds!)", "Compare Images", "Learn PCA","Feedback"]

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
    uploaded_image= st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_image:
        if validate_image(uploaded_image):
            st.image(uploaded_image, caption="Original Image", use_column_width=True)
            
            # Load the image
            img = Image.open(uploaded_image)
            img_byte = BytesIO()
            img.save(img_byte, format='JPEG')
            img_byte.seek(0)
            st.session_state['image'] = img_byte.getvalue()
        
            
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
            
def display_metrics(original_image, compressed_image):
    original_bytes = BytesIO()
    compressed_bytes = BytesIO()

    original_image.save(original_bytes, format='JPEG')
    compressed_image.save(compressed_bytes, format='JPEG')

    original_size = len(original_bytes.getvalue())
    compressed_size = len(compressed_bytes.getvalue())

    compression_ratio = compressed_size / original_size

    st.write(f"**Original Size:** {original_size / 1024:.2f} KB")
    st.write(f"**Compressed Size:** {compressed_size / 1024:.2f} KB")
    st.write(f"**Compression Ratio:** {compression_ratio:.2f}")

    original_array = np.array(original_image)
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
        display_metrics(original_image, compressed_image)
        
        st.subheader("Histograms")
        col3, col4 = st.columns(2)
        
        with col3:
            display_histogram(original_image, "Original Image Histogram")
        
        with col4:
            display_histogram(compressed_image, "Compressed Image Histogram")
            
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
            feedbacks.append(feedback_data)
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
        
def what_PCA():
    st.title("Learn PCA")

    st.markdown("""
    <style>
        .big-paragraph {
            font-size: 22px;
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
    </style>
    <p class="sub", style="font-size: 40px;">What is PCA?</p>
    <p class="big-paragraph">Two main mathematical vectors –</p>
    <p style="text-align:justify", class="big-paragraph">a.	Eigen Vector</p>
    <p style="text-align:justify", class="big-paragraph">b. Eigen Value</p>
    <p class= "big_paragraph">We know the Arabic numerals 0, 1, 2, …; and if we begin to arrange these numbers in the form of rows and columns and then add them like we add numerals and multiply them like we add numerals and multiply them like we do for numbers as follows:</p>
    """, unsafe_allow_html=True)
    st.latex(r"""\begin{bmatrix} 2 & 1 \\ 3 & 4 \end{bmatrix} + \begin{bmatrix} 8 & 1 \\ 9 & 6 \end{bmatrix} = \begin{bmatrix} 10 & 2 \\ 12 & 10 \end{bmatrix}\tag{1}""")
    st.markdown("""
    <p class="big_paragraph">Similarly, we can multiply them as follows:</p>
    """, unsafe_allow_html=True)
    st.latex(r"""\begin{bmatrix} 1 & 2 \\ 3 & 4 \end{bmatrix} \times \begin{bmatrix} 1 & 1 \\ 1 & 2 \end{bmatrix} = \begin{bmatrix} (1×1)+(2×1) & (1×1)+(2×2) \\ (3×1)+(4×1) & (3×1)+(4×2) \end{bmatrix} = \begin{bmatrix} 3 & 5 \\ 7 & 11 \end{bmatrix}\tag{2}""")
    st.markdown("""
                <p class="big_paragraph">What do we realise from equation (i) & (ii) above! The objects on the RHS are new matrices after adding or multiplying two matrices the way we have for numbers.</p>
                <p class="big_paragraph">Before we proceed, we can define one more multiplication of a matrix with a scalar as follows:</p>
                """, unsafe_allow_html=True)
    st.latex(r"""\begin{bmatrix} 5 & 1 \\ 6 & 1 \end{bmatrix} \times 2 = \begin{bmatrix} 10 & 2 \\ 12 & 2 \end{bmatrix}\tag{3}""")
    st.markdown("""
                <p class="big_paragraph">However, things start getting interesting when we start multiplying a matrix to a 𝕍𝔼ℂ𝕋𝕆ℝ. What does 𝕍𝔼ℂ𝕋𝕆ℝ mean.</p>
                <p class="big_paragraph">Well, any matrix with one row or column can be called as a vector. Graphically one can say that a matrix formed by the components of a vector in mutually perpendicular directions can be said to be a 𝕍𝔼ℂ𝕋𝕆ℝ.</p>
                <p class="big_paragraph">e.g.</p>
                """, unsafe_allow_html=True)
    st.image("Resources/img1.png", width=500)
    st.markdown("""<p class="big-paragraph", style="font-weight: bold;">•	Let’s play and see what matrix does to ‘VECTORS’?</p>""", unsafe_allow_html=True)
    st.latex(r"""Consider\space a\space matrix \begin{bmatrix} 3 & -2 \\ -1 & 4 \end{bmatrix} and\space a\space vector \begin{bmatrix} 1 \\ 2 \end{bmatrix}.""")
    st.markdown("""<p class="big_paragraph">Now, let’s multiply both of them and see what happens</p>""", unsafe_allow_html=True)
    st.latex(r"""\begin{bmatrix} 3 & -2 \\ -1 & 4 \end{bmatrix} \times \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 3×1 + (-2)×1 \\ -1×1 + 4×1 \end{bmatrix} = \begin{bmatrix} 1 \\ 3 \end{bmatrix}""")
    st.markdown("""<p class="big_paragraph">So, we put a vector as input and we get another vector as output but, that is scaled and rotated as compared to the original one. This is what it means that ‘Matrix Does Sometimes Interesting to Vectors.’</p>""", unsafe_allow_html=True)
    st.image("Resources/img2.png", width=500)
    st.markdown("""<p class="big_paragraph">Different matrices can scale and rotate the vectors into different vectors at all. Let us take a few following examples to understand this rotation dance:</p>""", unsafe_allow_html=True)
    st.markdown("""<p class="big_paragraph"><strong>✓</strong> 	The following matrix, if multiplied with a vector, will rotate the given vector by 90॰.</p>""", unsafe_allow_html=True)
    st.latex(r"""\begin{bmatrix} 0 & -1 \\ 1 & 0 \end{bmatrix} \times \begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} -1 \\ 2 \end{bmatrix}""")
    st.image("Resources/img3.png", width=500)
    st.markdown("""<p class="big_paragraph"><strong>✓</strong> 	The following matrix will scale the input matrix by a factor of 2, since the diagonal elements contain 2.</p>""", unsafe_allow_html=True)
    st.latex(r"""\begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix} \times \begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} 4 \\ 2 \end{bmatrix}""")
    st.image("Resources/img4.png", width=500)
    st.markdown("""<p class="big_paragraph">So, different input matrices get scaled and rotated differently based on how we operate upon them. However, all the transformation are linear as in any vector on the same line as one of those inputs will be mapped on the same line as the corresponding outputs.</p>""", unsafe_allow_html=True)
    st.latex(r"""\begin{bmatrix} 3 & -2 \\ -1 & 4 \end{bmatrix} \times \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 1 \\ 3 \end{bmatrix}""")
    st.image("Resources/img5.png", width=500)
    st.latex(r"""\begin{bmatrix} 3 & -2 \\ -1 & 4 \end{bmatrix} \times \begin{bmatrix} 3 \\ 3 \end{bmatrix} = \begin{bmatrix} 3 \\ 9 \end{bmatrix}""")
    st.image("Resources/img6.png", width=500)
    st.latex(r"""\text{Now consider a matrix A = }\begin{bmatrix} 3 & -2 \\ -1 & 4 \end{bmatrix} \text{and calculate it’s eigen value and eigen vectors which can be as follows:}""")
    st.latex(r"""\text{Eigen values come out to be 2 and 5 respectively and the corresponding eigen vectors are }\begin{bmatrix} 2 \\ 1 \end{bmatrix} \text{and} \begin{bmatrix} 1 \\ -1 \end{bmatrix}.""")
    st.latex(r"""\text{Now, let’s see what happens when we multiply the matrix A with it’s eigen vectors.}""")
    st.latex(r"""\begin{bmatrix} 3 & -2 \\ -1 & 4 \end{bmatrix} \times \begin{bmatrix} 2 \\ 1 \end{bmatrix} = \begin{bmatrix} 4 \\ 2 \end{bmatrix}""")
    st.image("Resources/img7.png", width=500)
    st.markdown("""<p class="big_paragraph">So, what we notice is that, we took a vector A.  We called it an eigen vector of matrix A. Then when we operate this vector with the matrix A, no change occurred in the direction although the same matrix A was responsible for rotating and scaling other vectors earlier. So, any vector that is only scaled by a matrix is called an <b>Eigen Vactor</b> <i>(Eigen in German means ‘Same’)</i> of that matrix, and how much the vector is scaled by is called its ‘Eigen Value.’ So, Eigen Vectors and Eigen Values are the vectors and values that remain unchanged in direction and only get scaled when operated upon by a matrix.</p>""", unsafe_allow_html=True)
    
    # Display the next button
    if st.button("**Feedback ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % len(pages)
        st.rerun()


if current_page == "Home":
    home()
elif current_page == "Compress Image":
    upload_image()
elif current_page == "How PCA Works (For Technerds!)":
    how_pca_works()
elif current_page == "Compare Images":
    comparison()
elif current_page == "Learn PCA":
    what_PCA()
elif current_page == "Feedback":
    feedback()


def generate_footer():
    return """
    <footer style="text-align: center; font-size: 14px; color: black;">
        This is the footer text. You can add any additional information or links here.
    </footer>
    """
