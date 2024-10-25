# how_pca_works.py

import streamlit as st
import numpy as np
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import time
import os

def set_custom_style():
    st.markdown("""
        <style>
        .tech-header {
            background: linear-gradient(to right, #4880EC, #019CAD);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .explanation-box {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #019CAD;
            margin: 20px 0;
        }
        .code-section {
            background-color: #f1f1f1;
            padding: 15px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .step-header {
            color: #4880EC;
            font-size: 20px;
            font-weight: bold;
            margin: 15px 0;
        }
        .info-box {
            background-color: #e7f3fe;
            border-left: 6px solid #2196F3;
            padding: 20px;
            margin: 20px 0;
        }
        .button-style {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .image-container {
            border: 2px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            margin: 10px 0;
        }
        .metrics-container {
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .metric-box {
            background-color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .metric-value {
            font-size: 24px;
            font-weight: bold;
            color: #4880EC;
        }
        .metric-label {
            font-size: 14px;
            color: #666;
        }
        </style>
    """, unsafe_allow_html=True)

def pca_compress(channel, no_of_components, channel_name):
    with st.container():
        st.markdown(f'<div class="step-header">{channel_name} Channel PCA:</div>', unsafe_allow_html=True)
        mean = np.mean(channel, axis=0)
        centered_data = channel - mean

        cov_matrix = np.cov(centered_data, rowvar=False)
        st.text(f'Step in {channel_name}: Covariance Matrix\n{cov_matrix}')

        eig_vals, eig_vecs = np.linalg.eigh(cov_matrix)

        sorted_indices = np.argsort(eig_vals)[::-1]
        sorted_eig_vals = eig_vals[sorted_indices]
        sorted_eig_vecs = eig_vecs[:, sorted_indices]

        st.text(f'Step in {channel_name}: Sorted Eigenvalues\n{sorted_eig_vals}')
        st.text(f'Step in {channel_name}: Sorted Eigenvectors\n{sorted_eig_vecs}')

        if no_of_components > len(sorted_eig_vals):
            no_of_components = len(sorted_eig_vals)
        elif no_of_components < 1:
            no_of_components = 1

        projection_matrix = sorted_eig_vecs[:, :no_of_components]
        compressed_data = np.dot(centered_data, projection_matrix)

        reconstructed_data = np.dot(compressed_data, projection_matrix.T) + mean

        reconstructed_display_data = (reconstructed_data - np.min(reconstructed_data)) / (np.max(reconstructed_data) - np.min(reconstructed_data))
        st.image(reconstructed_display_data, caption=f'Step in {channel_name}: Reconstructed Data', use_column_width=True)

        reconstructed_data = np.clip(reconstructed_data, 0, 255)

        return reconstructed_data.astype(np.uint8)

def apply_pca_to_image(original_image, no_of_components):

    # Start timing
    start_time = time.time()

    # Get original image size
    original_img_byte = BytesIO()
    original_image.save(original_img_byte, format='JPEG')
    original_size = len(original_img_byte.getvalue())
    
    with st.container():
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        img_array = np.array(original_image.convert("RGB"))
        st.image(img_array, caption='Original Image', use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="step-header">Channel Separation:</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    red_channel = img_array[:, :, 0]
    green_channel = img_array[:, :, 1]
    blue_channel = img_array[:, :, 2]

    with col1:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(red_channel, caption='Red Channel', use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(green_channel, caption='Green Channel', use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(blue_channel, caption='Blue Channel', use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with st.spinner('Applying PCA to each channel...'):
        red_compressed = pca_compress(red_channel, no_of_components, 'Red Channel')
        green_compressed = pca_compress(green_channel, no_of_components, 'Green Channel')
        blue_compressed = pca_compress(blue_channel, no_of_components, 'Blue Channel')

    compressed_img_array = np.stack((red_compressed, green_compressed, blue_compressed), axis=2)
    compressed_img = Image.fromarray(np.uint8(compressed_img_array))
    
    # Get compressed image size
    compressed_img_bytes = BytesIO()
    compressed_img.save(compressed_img_bytes, format='JPEG')
    compressed_size = len(compressed_img_bytes.getvalue())
    
    # Calculate compression ratio and time taken
    compression_ratio = (1 - compressed_size/original_size) * 100
    time_taken = time.time() - start_time

    # Display metrics in an organized way
    st.markdown("""
        <div class="step-header">Compression Metrics:</div>
        <div class="explanation-box">
    """, unsafe_allow_html=True)

    # Create three columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div style='text-align: center;'>
                <h4>Original Size</h4>
                <p>{:.2f} KB</p>
            </div>
        """.format(original_size/1024), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='text-align: center;'>
                <h4>Compressed Size</h4>
                <p>{:.2f} KB</p>
            </div>
        """.format(compressed_size/1024), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='text-align: center;'>
                <h4>Compression Ratio</h4>
                <p>{:.2f}%</p>
            </div>
        """.format(compression_ratio), unsafe_allow_html=True)

    # Additional metrics
    col4, col5 = st.columns(2)
    
    with col4:
        st.markdown("""
            <div style='text-align: center;'>
                <h4>Processing Time</h4>
                <p>{:.2f} seconds</p>
            </div>
        """.format(time_taken), unsafe_allow_html=True)
    
    with col5:
        st.markdown("""
            <div style='text-align: center;'>
                <h4>Principal Components Used</h4>
                <p>{}</p>
            </div>
        """.format(no_of_components), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Display final images
    st.markdown('<div class="step-header">Final Result:</div>', unsafe_allow_html=True)
    col6, col7 = st.columns(2)
    
    with col6:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(original_image, caption='Original Image', use_column_width=True)
        st.markdown(f"Size: {original_size/1024:.2f} KB", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col7:
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        st.image(compressed_img, caption='Compressed Image', use_column_width=True)
        st.markdown(f"Size: {compressed_size/1024:.2f} KB", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Add a download button for the compressed image
    st.download_button(
        label="Download Compressed Image",
        data=compressed_img_bytes.getvalue(),
        file_name="compressed_image.jpg",
        mime="image/jpeg"
    )

    return compressed_img_bytes

def how_pca_works_page():
    set_custom_style()

    # Enhanced Header
    st.markdown("""
        <div class="tech-header">
            <h1>📊 How PCA Works (For Technerds!)</h1>
            <p style='font-size: 18px;'>Dive deep into the technical implementation of PCA</p>
        </div>
    """, unsafe_allow_html=True)

    # Introduction Section
    st.markdown("""
        <div class="explanation-box">
            <h3>What This Section Offers:</h3>
            <p>This section provides a detailed, technical walkthrough of how PCA (Principal Component Analysis) 
            is implemented for image compression. You'll see:</p>
            <ul>
                <li>Step-by-step visualization of the PCA process</li>
                <li>Actual code implementation</li>
                <li>Real-time processing of your uploaded image</li>
                <li>Detailed mathematical computations at each step</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # Add Code Implementation Section
    st.markdown("""
        <div class="step-header">PCA Implementation Code:</div>
        <div class="explanation-box">
            <h4>Step 1: Image Preprocessing</h4>
            <p>First, we convert the image to a numpy array and split it into RGB channels:</p>
        </div>
    """, unsafe_allow_html=True)

    st.code("""
    # Convert image to numpy array
    img_array = np.array(image.convert("RGB"))
    
    # Split into RGB channels
    red_channel = img_array[:, :, 0]
    green_channel = img_array[:, :, 1]
    blue_channel = img_array[:, :, 2]
    """, language='python')

    st.markdown("""
        <div class="explanation-box">
            <h4>Step 2: PCA Compression Function</h4>
            <p>The core PCA implementation for each color channel:</p>
        </div>
    """, unsafe_allow_html=True)

    st.code("""
    def pca_compress(channel, num_components):
        # Calculate mean and center the data
        mean = np.mean(channel, axis=0)
        centered_data = channel - mean

        # Compute covariance matrix
        cov_matrix = np.cov(centered_data, rowvar=False)

        # Compute eigenvalues and eigenvectors
        eig_vals, eig_vecs = np.linalg.eigh(cov_matrix)

        # Sort eigenvalues and eigenvectors in descending order
        sorted_indices = np.argsort(eig_vals)[::-1]
        sorted_eig_vals = eig_vals[sorted_indices]
        sorted_eig_vecs = eig_vecs[:, sorted_indices]

        # Select top k eigenvectors
        projection_matrix = sorted_eig_vecs[:, :num_components]

        # Project data onto new basis
        compressed_data = np.dot(centered_data, projection_matrix)

        # Reconstruct the data
        reconstructed_data = np.dot(compressed_data, projection_matrix.T) + mean

        return np.clip(reconstructed_data, 0, 255).astype(np.uint8)
    """, language='python')

    st.markdown("""
        <div class="explanation-box">
            <h4>Step 3: Combining Channels</h4>
            <p>After compressing each channel, we combine them back into an RGB image:</p>
        </div>
    """, unsafe_allow_html=True)

    st.code("""
    # Compress each channel
    red_compressed = pca_compress(red_channel, num_components)
    green_compressed = pca_compress(green_channel, num_components)
    blue_compressed = pca_compress(blue_channel, num_components)

    # Stack channels back together
    compressed_img_array = np.stack(
        (red_compressed, green_compressed, blue_compressed), 
        axis=2
    )

    # Convert back to PIL Image
    compressed_img = Image.fromarray(np.uint8(compressed_img_array))
    """, language='python')

    st.markdown("""
        <div class="explanation-box">
            <h4>Mathematical Explanation:</h4>
            <ul>
                <li>PCA finds the directions (principal components) of maximum variance in the data</li>
                <li>The eigenvalues represent the amount of variance explained by each principal component</li>
                <li>By keeping only the top k components, we achieve dimensionality reduction while preserving the most important features</li>
                <li>The compression ratio is approximately original_dimensions/num_components</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

    # Upload Image section (existing code)
    uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_image:
        original_image = Image.open(uploaded_image)
        st.image(original_image, caption="Original Image", use_column_width=True)

        # Slider for choosing number of components
        num_components = st.slider("Number of Principal Components", min_value=1, max_value=500, value=10)

        if st.button("Apply PCA"):
            apply_pca_to_image(original_image, num_components)
            
    if st.button("**Compare Images ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % 7
        st.rerun()
