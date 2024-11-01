# image_analytics.py

import streamlit as st
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns
from skimage.metrics import structural_similarity as ssim
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.filters import sobel
from skimage.feature import canny
import cv2
from io import BytesIO
from scipy import stats
from skimage.color import rgb2lab, lab2rgb
import requests
import io
import base64
from pathlib import Path
import os
import datetime
import json

class ImageAnalytics:
    def __init__(self):
        self.style_config()

    def style_config(self):
        """Configure page styling"""
        st.markdown("""
            <style>
            .metric-card {
                background-color: #f0f2f6;
                padding: 20px;
                border-radius: 10px;
                margin: 10px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .explanation-text {
                font-size: 14px;
                color: #666;
                margin-top: 5px;
                line-height: 1.5;
            }
            .visualization-container {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                margin: 20px 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .header-text {
                color: #1E88E5;
                font-weight: bold;
                font-size: 24px;
                margin-bottom: 15px;
            }
            .subheader-text {
                color: #333;
                font-size: 18px;
                margin-bottom: 10px;
            }
            .metric-value {
                font-size: 24px;
                font-weight: bold;
                color: #1E88E5;
            }
            .download-button {
                background-color: #1E88E5;
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                border: none;
                cursor: pointer;
                margin: 10px 0;
            }
            .download-button:hover {
                background-color: #1976D2;
            }
            </style>
        """, unsafe_allow_html=True)

    def calculate_basic_metrics(self, original_img, compressed_img):
        """Calculate basic image quality metrics"""
        orig_array = np.array(original_img)
        comp_array = np.array(compressed_img)

        # SSIM calculation with multichannel support
        ssim_value = ssim(orig_array, comp_array, channel_axis=-1)
        
        # PSNR calculation
        psnr_value = psnr(orig_array, comp_array)
        
        # MSE calculation
        mse = np.mean((orig_array - comp_array) ** 2)
        
        # Color retention
        color_retention = self.calculate_color_retention(orig_array, comp_array)
        
        # Calculate entropy difference
        orig_entropy = self.calculate_entropy(orig_array)
        comp_entropy = self.calculate_entropy(comp_array)
        entropy_diff = abs(orig_entropy - comp_entropy)
        
        return {
            'ssim': ssim_value,
            'psnr': psnr_value,
            'mse': mse,
            'color_retention': color_retention,
            'entropy_diff': entropy_diff
        }

    def calculate_entropy(self, img_array):
        """Calculate image entropy"""
        histogram = np.histogram(img_array, bins=256, range=(0, 255))[0]
        histogram = histogram / np.sum(histogram)
        return -np.sum(histogram * np.log2(histogram + np.finfo(float).eps))

    def calculate_color_retention(self, img1, img2):
        """Calculate color retention percentage"""
        return np.mean(1 - np.abs(img1 - img2) / 255) * 100

    def analyze_color_distribution(self, original_img, compressed_img):
        """Analyze color distribution changes in L*a*b* color space"""
        orig_lab = rgb2lab(np.array(original_img) / 255.0)
        comp_lab = rgb2lab(np.array(compressed_img) / 255.0)
        
        l_diff = np.mean(np.abs(orig_lab[:,:,0] - comp_lab[:,:,0]))
        a_diff = np.mean(np.abs(orig_lab[:,:,1] - comp_lab[:,:,1]))
        b_diff = np.mean(np.abs(orig_lab[:,:,2] - comp_lab[:,:,2]))
        
        return {
            'lightness_diff': l_diff,
            'a_diff': a_diff,
            'b_diff': b_diff
        }

    def analyze_edge_preservation(self, original_img, compressed_img):
        """Analyze edge preservation using Canny edge detection"""
        orig_gray = cv2.cvtColor(np.array(original_img), cv2.COLOR_RGB2GRAY)
        comp_gray = cv2.cvtColor(np.array(compressed_img), cv2.COLOR_RGB2GRAY)
        
        orig_edges = canny(orig_gray)
        comp_edges = canny(comp_gray)
        
        edge_preservation = np.sum(comp_edges & orig_edges) / np.sum(orig_edges)
        return edge_preservation

    def analyze_texture_preservation(self, original_img, compressed_img):
        """Analyze texture preservation using Gabor filters"""
        def gabor_features(image):
            gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
            features = []
            for theta in range(0, 180, 45):
                kernel = cv2.getGaborKernel((21, 21), 4.0, theta, 10.0, 0.5, 0, ktype=cv2.CV_32F)
                filtered = cv2.filter2D(gray, cv2.CV_8UC3, kernel)
                features.append(np.mean(filtered))
            return np.array(features)
        
        orig_features = gabor_features(original_img)
        comp_features = gabor_features(compressed_img)
        
        texture_similarity = np.corrcoef(orig_features, comp_features)[0,1]
        return texture_similarity

    def plot_image_comparison(self, original_img, compressed_img):
        """Create comprehensive image comparison plots"""
        fig = plt.figure(figsize=(15, 12))
        
        # Original vs Compressed
        plt.subplot(331)
        plt.imshow(original_img)
        plt.title('Original Image')
        plt.axis('off')
        
        plt.subplot(332)
        plt.imshow(compressed_img)
        plt.title('Compressed Image')
        plt.axis('off')
        
        # Difference map
        plt.subplot(333)
        diff = np.abs(np.array(original_img) - np.array(compressed_img))
        plt.imshow(diff)
        plt.title('Difference Map')
        plt.colorbar()
        plt.axis('off')
        
        # Edge detection comparison
        orig_gray = cv2.cvtColor(np.array(original_img), cv2.COLOR_RGB2GRAY)
        comp_gray = cv2.cvtColor(np.array(compressed_img), cv2.COLOR_RGB2GRAY)
        
        plt.subplot(334)
        plt.imshow(canny(orig_gray), cmap='gray')
        plt.title('Original Edges')
        plt.axis('off')
        
        plt.subplot(335)
        plt.imshow(canny(comp_gray), cmap='gray')
        plt.title('Compressed Edges')
        plt.axis('off')
        
        # Histogram comparison
        plt.subplot(336)
        plt.hist(np.array(original_img).ravel(), bins=256, alpha=0.5, label='Original', density=True)
        plt.hist(np.array(compressed_img).ravel(), bins=256, alpha=0.5, label='Compressed', density=True)
        plt.title('Pixel Value Distribution')
        plt.legend()
        
        # Texture preservation
        plt.subplot(337)
        plt.imshow(original_img)
        plt.title('Original Texture')
        plt.axis('off')
        
        plt.subplot(338)
        plt.imshow(compressed_img)
        plt.title('Compressed Texture')
        plt.axis('off')
        
        # Entropy comparison
        plt.subplot(339)
        plt.bar(['Original', 'Compressed'], [self.calculate_entropy(np.array(original_img)), self.calculate_entropy(np.array(compressed_img))])
        plt.title('Entropy Comparison')
        plt.xlabel('Image')
        plt.ylabel('Entropy')
        
        plt.tight_layout()
        return fig
    

    def display_comparison(self):
        """Main function for image comparison page"""
        st.title("🔍 Advanced Image Analysis Dashboard")
        
        if 'compressed_image' not in st.session_state or 'original_image' not in st.session_state:
            st.warning("⚠️ Please compress an image first!")
            return

        # Load images
        original_img = Image.open(BytesIO(st.session_state.original_image))
        compressed_img = Image.open(BytesIO(st.session_state.compressed_image))

        # Side-by-side image comparison
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Original Image")
            st.image(original_img)
        with col2:
            st.subheader("Compressed Image")
            st.image(compressed_img)

        # Basic metrics
        st.header("📊 Image Quality Metrics")
        metrics = self.calculate_basic_metrics(original_img, compressed_img)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Structural Similarity (SSIM)", f"{metrics['ssim']:.4f}")
            st.markdown("""
                <div class='explanation-text'>
                SSIM measures how similar two images are structurally:
                - 1.0 = Perfect structural similarity
                - 0.0 = No structural similarity
                Values above 0.95 indicate excellent quality preservation.
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Peak Signal-to-Noise Ratio", f"{metrics['psnr']:.2f} dB")
            st.markdown("""
                <div class='explanation-text'> PSNR measures the ratio between maximum possible signal power and noise power:
                - Higher values indicate better quality
                - Typical values range from 20 dB (low quality) to 40 dB (high quality)
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Mean Squared Error (MSE)", f"{metrics['mse']:.2f}")
            st.markdown("""
                <div class='explanation-text'>MSE measures the average squared difference between pixels:
                - Lower values indicate better compression
                - Typical values range from 0 (perfect compression) to 255 (no compression)
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Color Retention", f"{metrics['color_retention']:.2f}%")
            st.markdown("""
                <div class='explanation-text'>Color retention measures the percentage of color information preserved:
                - Higher values indicate better color preservation
                - Typical values range from 0% (no color preservation) to 100% (perfect color preservation)
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Advanced analytics
        st.header("🔍 Advanced Image Analysis")
        color_diff = self.analyze_color_distribution(original_img, compressed_img)
        edge_preservation = self.analyze_edge_preservation(original_img, compressed_img)
        texture_similarity = self.analyze_texture_preservation(original_img, compressed_img)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='metric-card'>", unsafe_allow_html =True)
            st.metric("Lightness Difference", f"{color_diff['lightness_diff']:.2f}")
            st.markdown("""
                <div class='explanation-text'>Lightness difference measures the average difference in lightness between images:
                - Lower values indicate better lightness preservation
                - Typical values range from 0 (perfect lightness preservation) to 100 (no lightness preservation)
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Edge Preservation", f"{edge_preservation:.2f}")
            st.markdown("""
                <div class='explanation-text'>Edge preservation measures the percentage of edges preserved:
                - Higher values indicate better edge preservation
                - Typical values range from 0% (no edge preservation) to 100% (perfect edge preservation)
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("a* Difference", f"{color_diff['a_diff']:.2f}")
            st.markdown("""
                <div class='explanation-text'>a* difference measures the average difference in a* color channel between images:
                - Lower values indicate better a* color preservation
                - Typical values range from 0 (perfect a* color preservation) to 100 (no a* color preservation)
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("b* Difference", f"{color_diff['b_diff']:.2f}")
            st.markdown("""
                <div class='explanation-text'>b* difference measures the average difference in b* color channel between images:
                - Lower values indicate better b* color preservation
                - Typical values range from 0 (perfect b* color preservation) to 100 (no b* color preservation)
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Texture Similarity", f"{texture_similarity:.2f}")
            st.markdown("""
                <div class='explanation-text'>Texture similarity measures the correlation between texture features:
                - Higher values indicate better texture preservation
                - Typical values range from 0 (no texture preservation) to 1 (perfect texture preservation)
                </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Comprehensive image comparison plots
        st.header("📊 Comprehensive Image Comparison")
        comparison_fig = self.plot_image_comparison(original_img, compressed_img)
        st.pyplot(comparison_fig)

        # Download buttons
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                "Download Original Image",
                st.session_state.original_image,
                "original_image.jpg",
                "image/jpeg"
            )
        with col2:
            st.download_button(
                "Download Compressed Image",
                st.session_state.compressed_image,
                "compressed_image.jpg",
                "image/jpeg"
            )
    @staticmethod
    def comparison():
        """Main function to be called from app.py"""
        analytics = ImageAnalytics()
        analytics.display_comparison()      
        
def comparison():
    ImageAnalytics.comparison()

    # Display the next button
    if st.button("**Learn PCA ⇨**", key="next"):
        st.session_state.page_index = (st.session_state.page_index + 1) % 7
        st.rerun()  