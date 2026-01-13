import numpy as np
import cv2
import matplotlib
matplotlib.use('Agg') # Non-interactive backend
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
from skimage.filters import sobel
from skimage.color import rgb2lab
from skimage.feature import local_binary_pattern
import io
import base64

def array_to_base64_plot(plot_func, *args, **kwargs):
    """Helper to run a plotting function and return base64 string"""
    plt.figure()
    plot_func(*args, **kwargs)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def get_ssim(img1, img2):
    # img1, img2 are numpy arrays (RGB)
    # Convert to grayscale for SSIM
    g1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
    g2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    
    # win_size must be odd and <= min dim
    min_dim = min(g1.shape[0], g1.shape[1])
    win_size = min(7, min_dim)
    if win_size % 2 == 0: win_size -= 1
    
    score, diff = ssim(g1, g2, full=True, win_size=win_size)
    return score, diff

def get_sharpness(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    return np.var(laplacian)

def generate_histograms(img1, img2):
    # Returns base64 image of side-by-side histograms
    def plot():
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
        ax1.hist(img1.ravel(), bins=256, color='blue', alpha=0.7)
        ax1.set_title("Original Histogram")
        ax2.hist(img2.ravel(), bins=256, color='red', alpha=0.7)
        ax2.set_title("Compressed Histogram")
        plt.tight_layout()
    
    return array_to_base64_plot(plot)

def generate_channel_histograms(img1, img2):
    def plot():
        fig, axs = plt.subplots(2, 3, figsize=(12, 6))
        colors = ['red', 'green', 'blue']
        for i, color in enumerate(colors):
            axs[0, i].hist(img1[:, :, i].ravel(), bins=256, color=color, alpha=0.5)
            axs[0, i].set_title(f'Original {color.title()}')
            axs[1, i].hist(img2[:, :, i].ravel(), bins=256, color=color, alpha=0.5)
            axs[1, i].set_title(f'Compressed {color.title()}')
        plt.tight_layout()
    return array_to_base64_plot(plot)

def generate_pixel_intensity(img1, img2):
    def plot():
        g1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        g2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
        plt.figure(figsize=(8, 4))
        plt.hist(g1.ravel(), bins=256, color='blue', alpha=0.5, label='Original')
        plt.hist(g2.ravel(), bins=256, color='red', alpha=0.5, label='Compressed')
        plt.legend()
        plt.title('Pixel Intensity Overlay')
    return array_to_base64_plot(plot)

def generate_edges(img1, img2):
    def plot():
        g1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
        g2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
        e1 = sobel(g1)
        e2 = sobel(g2)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        ax1.imshow(e1, cmap='gray')
        ax1.set_title("Original Edges")
        ax1.axis('off')
        ax2.imshow(e2, cmap='gray')
        ax2.set_title("Compressed Edges")
        ax2.axis('off')
    return array_to_base64_plot(plot)

def generate_ssim_map(diff):
    def plot():
        plt.figure(figsize=(6, 6))
        plt.imshow(diff, cmap='gray')
        plt.title("SSIM Difference Map")
        plt.axis('off')
    return array_to_base64_plot(plot)

def generate_fft(img1, img2):
    def get_fft(img):
        g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        f = np.fft.fft2(g)
        fshift = np.fft.fftshift(f)
        return 20 * np.log(np.abs(fshift))
    
    def plot():
        f1 = get_fft(img1)
        f2 = get_fft(img2)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        ax1.imshow(f1, cmap='gray')
        ax1.set_title("Original FFT")
        ax1.axis('off')
        ax2.imshow(f2, cmap='gray')
        ax2.set_title("Compressed FFT")
        ax2.axis('off')
    return array_to_base64_plot(plot)

def generate_contours(img1, img2):
    def plot_cnt(img, ax, title):
        g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        ax.contour(g, cmap='viridis')
        ax.set_title(title)
        ax.invert_yaxis() # Contours often flip
        ax.axis('off')

    def plot():
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        plot_cnt(img1, ax1, "Original Contours")
        plot_cnt(img2, ax2, "Compressed Contours")
    return array_to_base64_plot(plot)

def generate_color_diff(img1, img2):
    # This is heavy
    def plot():
        lab1 = rgb2lab(img1)
        lab2 = rgb2lab(img2)
        diff = np.abs(lab1 - lab2)
        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4))
        ax1.imshow(diff[:,:,0], cmap='gray'); ax1.set_title("L* Diff"); ax1.axis('off')
        ax2.imshow(diff[:,:,1], cmap='gray'); ax2.set_title("a* Diff"); ax2.axis('off')
        ax3.imshow(diff[:,:,2], cmap='gray'); ax3.set_title("b* Diff"); ax3.axis('off')
    
    return array_to_base64_plot(plot)

def generate_texture(img1, img2):
    def get_lbp(img):
        g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        return local_binary_pattern(g, 8, 3, method='uniform')
    
    def plot():
        l1 = get_lbp(img1)
        l2 = get_lbp(img2)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        ax1.imshow(l1, cmap='gray'); ax1.set_title("Original Texture"); ax1.axis('off')
        ax2.imshow(l2, cmap='gray'); ax2.set_title("Compressed Texture"); ax2.axis('off')
    return array_to_base64_plot(plot)
