# Detailed Workings of PCA

"""

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
