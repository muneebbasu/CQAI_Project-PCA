from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse
import numpy as np
from PIL import Image
import io
import pydantic
import base64

app = FastAPI()

# Configure CORS for Next.js (Port 3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Processing-Time"],
)

# Initialize Database
from backend.database import FeedbackStorage
db = FeedbackStorage()

@app.get("/feedback")
def get_feedback():
    return db.get_recent_feedback(limit=50)

class FeedbackModel(pydantic.BaseModel):
    name: str
    rating: float
    comment: str

@app.post("/feedback")
def submit_feedback(feedback: FeedbackModel):
    db.save_feedback(feedback.name, feedback.rating, feedback.comment)
    return {"message": "Feedback saved"}

def pca_compress_channel(channel, no_of_components):
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

    # Analysis data (for How It Works)
    # Convert simple types for JSON
    analysis = {
        "cov_matrix": cov_matrix.tolist(), # Warning: Large!
        "eigenvalues": sorted_eig_vals.tolist(),
        "eigenvectors": sorted_eig_vecs.tolist() # Warning: Large!
    }

    # Select top k eigenvectors
    k = min(no_of_components, len(sorted_eig_vals))
    projection_matrix = sorted_eig_vecs[:, :k]

    # Project data onto new basis
    compressed_data = np.dot(centered_data, projection_matrix)

    # Reconstruct the data
    reconstructed_data = np.dot(compressed_data, projection_matrix.T) + mean
    
    return np.clip(reconstructed_data, 0, 255).astype(np.uint8), analysis

@app.post("/compress")
async def compress_image(image: UploadFile = File(...), num_components: int = Form(...)):
    import time
    start_time = time.perf_counter()
    
    contents = await image.read()
    img = Image.open(io.BytesIO(contents)).convert('RGB')
    img_array = np.array(img)

    red_channel = img_array[:, :, 0]
    green_channel = img_array[:, :, 1]
    blue_channel = img_array[:, :, 2]

    red_compressed, _ = pca_compress_channel(red_channel, num_components)
    green_compressed, _ = pca_compress_channel(green_channel, num_components)
    blue_compressed, _ = pca_compress_channel(blue_channel, num_components)

    compressed_img_array = np.stack(
        (red_compressed, green_compressed, blue_compressed), 
        axis=2
    )

    compressed_pil = Image.fromarray(compressed_img_array)
    img_byte_arr = io.BytesIO()
    # Quality 60 to ensure we actually see file size reduction vs original
    compressed_pil.save(img_byte_arr, format='JPEG', quality=60, optimize=True)
    
    process_time = time.perf_counter() - start_time
    
    return Response(
        content=img_byte_arr.getvalue(), 
        media_type="image/jpeg",
        headers={"X-Processing-Time": f"{process_time:.4f}"}
    )

@app.post("/analyze")
async def analyze_image(image: UploadFile = File(...)):
    import time
    start_time = time.perf_counter()
    
    # Limit size for analysis to avoid crashing browser with massive JSON
    contents = await image.read()
    img = Image.open(io.BytesIO(contents)).convert('RGB')
    
    # Resize for analysis speed (similar to what user wanted, but now in Python)
    # Python is fast, but sending 1000x1000 matrix over JSON is slow.
    # We will resize to small dimension for "Instructional" analysis.
    img.thumbnail((32, 32)) 
    img_array = np.array(img)

    red_channel = img_array[:, :, 0]
    green_channel = img_array[:, :, 1]
    blue_channel = img_array[:, :, 2]

    # We just need analysis from one channel or all? Let's do all.
    # Num components doesn't matter for analysis of full matrix, but the function needs it.
    # We pass full width to get full decomposition.
    k = img_array.shape[1] 
    
    _, r_analysis = pca_compress_channel(red_channel, k)
    _, g_analysis = pca_compress_channel(green_channel, k)
    _, b_analysis = pca_compress_channel(blue_channel, k)

    def sample_matrix(m):
        # Return top 5x5 subset for display
        return [row[:5] for row in m[:5]]

    process_time = time.perf_counter() - start_time

    return JSONResponse({
        "time": process_time,
        "red": {
            "cov": sample_matrix(r_analysis["cov_matrix"]),
            "eigVals": r_analysis["eigenvalues"][:10],
            "eigVecs": sample_matrix(r_analysis["eigenvectors"])
        },
        "green": {
             "cov": sample_matrix(g_analysis["cov_matrix"]),
             "eigVals": g_analysis["eigenvalues"][:10],
             "eigVecs": sample_matrix(g_analysis["eigenvectors"])
        },
        "blue": {
             "cov": sample_matrix(b_analysis["cov_matrix"]),
             "eigVals": b_analysis["eigenvalues"][:10],
             "eigVecs": sample_matrix(b_analysis["eigenvectors"])
        }
    })

@app.post("/compare/analytics")
async def compare_analytics(original: UploadFile = File(...), compressed: UploadFile = File(...)):
    import backend.analytics as ana
    import time
    
    start_time = time.perf_counter()
    
    # Read Images
    org_bytes = await original.read()
    comp_bytes = await compressed.read()
    
    img1 = np.array(Image.open(io.BytesIO(org_bytes)).convert('RGB'))
    img2 = np.array(Image.open(io.BytesIO(comp_bytes)).convert('RGB'))

    # Ensure same size for pixel-wise comparison (resize compressed to original if needed)
    if img1.shape != img2.shape:
        # Resize img2 to match img1
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Analysis
    ssim_score, diff_map = ana.get_ssim(img1, img2)
    sharp1 = ana.get_sharpness(img1)
    sharp2 = ana.get_sharpness(img2)
    
    plots = {
        "histograms": ana.generate_histograms(img1, img2),
        "channels": ana.generate_channel_histograms(img1, img2),
        "intensity": ana.generate_pixel_intensity(img1, img2),
        "edges": ana.generate_edges(img1, img2),
        "ssim_map": ana.generate_ssim_map(diff_map),
        "fft": ana.generate_fft(img1, img2),
        "contours": ana.generate_contours(img1, img2), # Can be slow
        "color_diff": ana.generate_color_diff(img1, img2),
        "texture": ana.generate_texture(img1, img2),
    }

    process_time = time.perf_counter() - start_time

    return JSONResponse({
        "metrics": {
            "ssim": float(ssim_score),
            "sharpness_original": float(sharp1),
            "sharpness_compressed": float(sharp2),
            "time": process_time
        },
        "plots": plots
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
