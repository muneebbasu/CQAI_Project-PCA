from PIL import Image
import numpy as np
from io import BytesIO

# Function to apply PCA on image
def apply_pca(img, num_components):
    # Convert image to numpy array
    img_array = np.array(img)

    # Splitting RGB channels
    red_channel = img_array[:, :, 0]
    green_channel = img_array[:, :, 1]
    blue_channel = img_array[:, :, 2]

    # Apply PCA on each channel
    red_compressed = pca_compress(red_channel, num_components)
    green_compressed = pca_compress(green_channel, num_components)
    blue_compressed = pca_compress(blue_channel, num_components)

    # Combine compressed channels into one image
    compressed_img_array = np.stack((red_compressed, green_compressed, blue_compressed), axis=2)

    # Convert back to image
    compressed_img = Image.fromarray(np.uint8(compressed_img_array))

    # Convert compressed image to BytesIO for storage
    compressed_img_bytes = BytesIO()
    compressed_img.save(compressed_img_bytes, format='JPEG')
    compressed_img_bytes.seek(0) 
    return compressed_img_bytes

# Function to perform PCA compression on a single channel
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

# Function to validate image format
def validate_image(uploaded_file):
    allowed_extensions = ["jpg", "jpeg", "png"]
    file_extension = uploaded_file.name.split(".")[-1].lower()
    if file_extension in allowed_extensions:
        return True
    else:
        return False
