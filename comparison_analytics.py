import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import cv2
from skimage.metrics import structural_similarity as ssim
from skimage.filters import sobel
from skimage.color import rgb2lab
from scipy import stats

def comparison_page():
    st.title("🖼️ Compare Images")

    st.markdown("""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h2 style="color: #1f77b4;">Welcome to the Image Comparison Section</h2>
        <p style="font-size: 16px;">
            This section allows you to compare your original image with its PCA-compressed version. 
            You'll learn about various image analysis techniques and how compression affects different 
            aspects of an image. This knowledge is crucial for understanding the trade-offs in image 
            compression and the practical applications of PCA in image processing.
        </p>
        <p style="font-size: 16px;">
            What you'll learn:
            <ul>
                <li>How compression affects image size and quality</li>
                <li>Changes in color distribution and intensity</li>
                <li>Effects on image edges and structural similarity</li>
                <li>Frequency domain analysis and its implications</li>
                <li>Advanced color space comparisons</li>
            </ul>
        </p>
    </div>
    """, unsafe_allow_html=True)

    if 'original_image' in st.session_state and 'compressed_image' in st.session_state:
        original_image = Image.open(st.session_state['original_image'])
        compressed_image = Image.open(st.session_state['compressed_image'])

        col1, col2 = st.columns(2)
        with col1:
            st.image(original_image, caption="Original Image", use_container_width=True)
        with col2:
            st.image(compressed_image, caption="Compressed Image", use_container_width=True)

        display_metrics(st.session_state['original_image'], st.session_state['compressed_image'])
        display_histograms(original_image, compressed_image)
        display_pixel_intensity_comparison(original_image, compressed_image)
        display_color_channel_comparison(original_image, compressed_image)
        display_edge_detection_comparison(original_image, compressed_image)
        display_ssim_map(original_image, compressed_image)
        display_frequency_domain_analysis(original_image, compressed_image)
        display_contour_plots(original_image, compressed_image)
        display_color_difference_maps(original_image, compressed_image)
        display_sharpness_comparison(original_image, compressed_image)
        display_texture_analysis(original_image, compressed_image)
    else:
        st.write("No images stored for comparison. Please compress an image first.")

def display_metrics(original_file, compressed_image):
    st.markdown("""
    ## 📊 Image Metrics
    These metrics provide a quantitative comparison between the original and compressed images.
    """)

    original_size = original_file.size
    compressed_bytes = compressed_image.getvalue()
    compressed_size = len(compressed_bytes)
    compression_ratio = original_size / compressed_size

    col1, col2, col3 = st.columns(3)
    col1.metric("Original Size", f"{original_size / 1024:.2f} KB")
    col2.metric("Compressed Size", f"{compressed_size / 1024:.2f} KB")
    col3.metric("Compression Ratio", f"{compression_ratio:.2f}")

    st.markdown("""
    - **Original Size**: The file size of the uploaded image.
    - **Compressed Size**: The file size after PCA compression.
    - **Compression Ratio**: How many times smaller the compressed image is compared to the original.
    
    A higher compression ratio indicates more space saved, but might come at the cost of image quality.
    """)

    original_array = np.array(Image.open(original_file))
    compressed_array = np.array(Image.open(compressed_image))
    win_size = min(original_array.shape[0], original_array.shape[1], 7)
    ssim_index = ssim(original_array, compressed_array, win_size=win_size, channel_axis=-1)

    st.metric("SSIM (Structural Similarity Index)", f"{ssim_index:.4f}")
    st.markdown("""
    **SSIM**: Measures the perceived similarity between two images. 
    - Ranges from -1 to 1, where 1 indicates perfect similarity.
    - Values above 0.9 generally indicate good quality compression.
    """)

def display_histograms(original_image, compressed_image):
    st.markdown("""
    ## 📊 Image Histograms
    Histograms show the distribution of pixel intensities in an image.
    """)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    ax1.hist(np.array(original_image).ravel(), bins=256, color='blue', alpha=0.7)
    ax1.set_title("Original Image Histogram")
    ax1.set_xlabel("Pixel Intensity")
    ax1.set_ylabel("Frequency")

    ax2.hist(np.array(compressed_image).ravel(), bins=256, color='red', alpha=0.7)
    ax2.set_title("Compressed Image Histogram")
    ax2.set_xlabel("Pixel Intensity")
    ax2.set_ylabel("Frequency")

    st.pyplot(fig)

    st.markdown("""
    - These histograms show how pixel intensities are distributed in both images.
    - Changes in the histogram shape can indicate alterations in contrast and brightness.
    - A well-preserved histogram suggests that the overall visual characteristics are maintained after compression.
    """)

def display_pixel_intensity_comparison(original_image, compressed_image):
    st.markdown("""
    ## 🔍 Pixel Intensity Comparison
    This analysis compares the distribution of pixel intensities between the original and compressed images.
    """)

    original_array = np.array(original_image.convert("L"))
    compressed_array = np.array(compressed_image.convert("L"))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(original_array.ravel(), bins=256, color='blue', alpha=0.5, label='Original')
    ax.hist(compressed_array.ravel(), bins=256, color='red', alpha=0.5, label='Compressed')
    ax.set_title('Pixel Intensity Distribution Comparison')
    ax.set_xlabel('Pixel Intensity')
    ax.set_ylabel('Frequency')
    ax.legend()
    st.pyplot(fig)

    st.markdown("""
    - This graph overlays the histograms of both images.
    - Significant differences can indicate changes in brightness, contrast, or overall tone.
    - Ideally, the compressed image should closely follow the original's distribution.
    """)

def display_color_channel_comparison(original_image, compressed_image):
    st.markdown("""
    ## 🌈 Color Channel Comparison
    This section breaks down the image into its Red, Green, and Blue components.
    """)

    original_array = np.array(original_image)
    compressed_array = np.array(compressed_image)

    fig, axs = plt.subplots(2, 3, figsize=(15, 10 ))

    for i, color in enumerate(['Red', 'Green', 'Blue']):
        axs[0, i].hist(original_array[:, :, i].ravel(), bins=256, color=color.lower(), alpha=0.5)
        axs[0, i].set_title(f'Original {color} Channel Histogram')

        axs[1, i].hist(compressed_array[:, :, i].ravel(), bins=256, color=color.lower(), alpha=0.5)
        axs[1, i].set_title(f'Compressed {color} Channel Histogram')

    st.pyplot(fig)

    st.markdown("""
    - Each color channel's histogram is shown for both images.
    - Changes in these histograms can indicate color shifts or loss of detail.
    - Ideally, the compressed image's color channels should closely match the original's.
    """)

def display_edge_detection_comparison(original_image, compressed_image):
    st.markdown("""
    ## 🔍 Edge Detection Comparison
    This analysis highlights the edges in both images using the Sobel operator.
    """)

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

    st.markdown("""
    - Edges are crucial for image perception and understanding.
    - The Sobel operator detects edges by calculating the gradient magnitude.
    - A well-preserved edge structure in the compressed image is essential for maintaining visual quality.
    """)

def display_ssim_map(original_image, compressed_image):
    st.markdown("""
    ## 🗺️ SSIM Map
    This map visualizes the structural similarity between the original and compressed images.
    """)

    original_array = np.array(original_image.convert("L"))
    compressed_array = np.array(compressed_image.convert("L"))

    ssim_index, ssim_image = ssim(original_array, compressed_array, full=True)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(ssim_image, cmap='gray')
    ax.set_title(f'SSIM Map (Score: {ssim_index:.4f})')
    st.pyplot(fig)


    st.markdown("""
    - The SSIM map highlights areas of high and low similarity.
    - A higher SSIM score indicates better preservation of structural information.
    - This map can help identify regions where compression has affected image quality.
    """)

def display_frequency_domain_analysis(original_image, compressed_image):
    st.markdown("""
    ## 📊 Frequency Domain Analysis
    This analysis transforms the images into the frequency domain using the FFT.
    """)

    def fft_image(image):
        image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        f_transform = np.fft.fft2(image_gray)
        f_shift = np.fft.fftshift(f_transform)
        magnitude_spectrum = 20 * np.log(np.abs(f_shift))
        return magnitude_spectrum

    original_fft = fft_image(original_image)
    compressed_fft = fft_image(compressed_image)

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

    st.markdown("""
    - The frequency domain representation shows the distribution of energy across different frequencies.
    - Changes in this distribution can indicate loss of high-frequency details.
    - A well-preserved frequency domain suggests that the compressed image maintains its original characteristics.
    """)

def display_contour_plots(original_image, compressed_image):
    st.markdown("""
    ## 📊 Contour Plots
    This analysis visualizes the contours of both images.
    """)

    def contour_plot(image, title):
        image_gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        plt.figure(figsize=(5, 3))
        plt.contour(image_gray, cmap='viridis')
        plt.title(title)
        plt.axis('off')
        st.pyplot(plt)

    col1, col2 = st.columns(2)
    with col1:
        contour_plot(original_image, "Original Image Contours")
    with col2:
        contour_plot(compressed_image, "Compressed Image Contours")

    st.markdown("""
    - Contours highlight the boundaries and shapes within an image.
    - A well-preserved contour structure in the compressed image is essential for maintaining visual quality.
    """)

def display_color_difference_maps(original_image, compressed_image):
    st.markdown("""
    ## 🌈 Color Difference Maps
    This analysis calculates the difference in color between the original and compressed images.
    """)

    original_lab = rgb2lab(np.array(original_image))
    compressed_lab = rgb2lab(np.array(compressed_image))
    
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

    st.markdown("""
    - These maps show the absolute difference in color between the original and compressed images.
    - A lower difference indicates better color preservation.
    """)

def display_sharpness_comparison(original_image, compressed_image):
    st.markdown("""
    ## 🔍 Sharpness Comparison
    This analysis compares the sharpness of both images using the Laplacian operator.
    """)

    def image_sharpness(image):
        gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
        sharpness = np.var(laplacian)
        return sharpness

    original_sharpness = image_sharpness(original_image)
    compressed_sharpness = image_sharpness(compressed_image)

    st.write(f"**Original Image Sharpness**: {original_sharpness:.2f}")
    st.write(f"**Compressed Image Sharpness**: {compressed_sharpness:.2f}")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Original Image**")
        st.image(original_image, caption=f"Sharpness: {original_sharpness:.2f}", use_container_width=True)
    with col2:
        st.write("**Compressed Image**")
        st.image(compressed_image, caption=f"Sharpness: {compressed_sharpness:.2f}", use_container_width=True)

    st.markdown("""
    - Sharpness is a measure of the image's clarity and detail.
    - A higher sharpness value indicates a clearer image.
    """)

def display_texture_analysis(original_image, compressed_image):
    st.markdown("""
    ## 🔍 Texture Analysis
    This analysis compares the texture of both images using the Local Binary Patterns (LBP) operator.
    """)

    from skimage.feature import local_binary_pattern

    original_gray = np.array(original_image.convert("L"))
    compressed_gray = np.array(compressed_image.convert("L"))

    original_lbp = local_binary_pattern(original_gray, 8, 3, method='uniform')
    compressed_lbp = local_binary_pattern(compressed_gray, 8, 3, method='uniform')

    fig, (ax1, ax2) = plt.subplots (1, 2, figsize=(12, 6))

    ax1.imshow(original_lbp, cmap='gray')
    ax1.set_title('Original Image Texture')

    ax2.imshow(compressed_lbp, cmap='gray')
    ax2.set_title('Compressed Image Texture')

    st.pyplot(fig)

    st.markdown("""
    - Texture is an essential aspect of image perception.
    - The LBP operator highlights the texture patterns in both images.
    - A well-preserved texture structure in the compressed image is crucial for maintaining visual quality.
    """)
    
        # Display the next button
    if st.button("**Learn PCA ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % 7
        st.rerun()   