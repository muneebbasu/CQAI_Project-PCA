from PIL import Image
import numpy as np
from io import BytesIO
from sklearn.decomposition import PCA

# Function to apply PCA on image
def apply_pca(img, num_components):
    # Convert image to numpy array
    img_array = np.array(img)

    # Splitting RGB channels
    red_channel = img_array[:, :, 0]
    green_channel = img_array[:, :, 1]
    blue_channel = img_array[:, :, 2]

    # Apply PCA on each channel
    pca = PCA(n_components=num_components)
    red_compressed = pca.fit_transform(red_channel.reshape(-1, 1))
    green_compressed = pca.fit_transform(green_channel.reshape(-1, 1))
    blue_compressed = pca.fit_transform(blue_channel.reshape(-1, 1))

    # Combine the compressed channels into one image
    compressed_img_array = np.stack((red_compressed, green_compressed, blue_compressed), axis=2)

    # Convert back to image
    compressed_img = Image.fromarray(np.uint8(compressed_img_array))

    # Convert compressed image to BytesIO for storage
    compressed_img_bytes = BytesIO()
    compressed_img.save(compressed_img_bytes, format='JPEG')
    compressed_img_bytes.seek(0)
    return compressed_img_bytes

# Function to validate image format
def validate_image(uploaded_file):
    allowed_extensions = ["jpg", "jpeg", "png"]
    file_extension = uploaded_file.name.split(".")[-1].lower()
    if file_extension in allowed_extensions:
        return True
    else:
        return False
