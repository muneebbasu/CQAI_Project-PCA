import streamlit as st
from PIL import Image
from io import BytesIO
import numpy as np
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt
import cv2
from skimage.color import rgb2lab, lab2rgb

st.sidebar.header(" NAVIGATION", divider='rainbow')

pages = ["Home", "Compress Image", "How PCA Works (For Technerds!)", "Compare Images", "Learn PCA","Feedback"]

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