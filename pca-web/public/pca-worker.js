
import { SVD } from 'ml-matrix';

self.onmessage = async (e) => {
    const { imageData, numComponents, width, height } = e.data;

    try {
        const { newData, analysis } = applyPCA(imageData, numComponents, width, height);
        self.postMessage({ type: 'success', result: newData, analysis: analysis, width, height });
    } catch (error) {
        self.postMessage({ type: 'error', error: error.message });
    }
};

function applyPCA(imageData, k, width, height) {
    // Separate channels
    const r = new Float64Array(width * height);
    const g = new Float64Array(width * height);
    const b = new Float64Array(width * height);

    for (let i = 0; i < width * height; i++) {
        r[i] = imageData[i * 4];
        g[i] = imageData[i * 4 + 1];
        b[i] = imageData[i * 4 + 2];
    }

    // Helper to process one channel
    const processChannel = (data) => {
        // Convert 1D array to Matrix (height x width)
        // ml-matrix expects 2D array for SVD? It handles basic arrays? 
        // Actually SVD constructs from Matrix. We need to create a Matrix-like structure or array of arrays.
        const matrixData = [];
        for (let i = 0; i < height; i++) {
            matrixData.push(Array.from(data.slice(i * width, (i + 1) * width)));
        }

        // Centering
        const mean = new Float64Array(width); // Mean of each column? 
        // Python code: mean = np.mean(channel, axis=0) -> mean of each column (across rows).
        // Result is size (width).

        for (let j = 0; j < width; j++) {
            let sum = 0;
            for (let i = 0; i < height; i++) {
                sum += matrixData[i][j];
            }
            mean[j] = sum / height;
        }

        // Center data
        const centered = matrixData.map(row => row.map((val, j) => val - mean[j]));

        // SVD (Optimized: We use Covariance method below, skipping direct SVD on data)
        // const svd = new SVD(centered, { autoTranspose: true });
        // ml-matrix 3.x+ : subMatrix(startRow, endRow, startCol, endCol)

        // Project: Z = X * V_k
        // Reconstruct: X_hat = Z * V_k^T + mean

        // Let's do raw matrix math for performance if possible, but ml-matrix objects are safer.
        // Matrix multiplication:
        // We need to convert `centered` to Matrix object first if not already.
        // SVD constructor took generic array, but we need Matrix methods now.

        // Note: This logic is computationally heavy in JS for large images.
        // We strictly use K components.

        // Optimization: If k is small, we don't need full SVD? 
        // But `ml - matrix` SVD usually computes full.
        // Randomized PCA is better for large matrices but complex to implement from scratch.

        // Let's proceed with standard SVD.
        // NOTE: If image is 1000x1000, 1M elements. SVD on 1000x1000 matrix is doable in JS.

        // Reconstruct
        const X = new SVD(centered); // Re-instantiate? No, utilize `svd` object.
        // Wait, `svd.U`, `svd.S`, `svd.V`.
        // We need to reconstruct manually.
        // X ~ U_k * S_k * V_k'

        // But Python code uses Eigendecomposition of Covariance Matrix!
        // Python: cov = np.cov(centered, rowvar=False) (shape width x width)
        // eig_vals, eig_vecs = np.linalg.eigh(cov)
        // This is MUCH faster if height >> width.
        // If we have 1000x1000, it's same.
        // But if we have 5000x5000...

        // Let's implement the Covariance method as it matches the Python code EXACTLY and is educational content.
        // 1. Covariance Matrix (width x width)
        // `centers` is Height x Width

        const w = width;
        const h = height;

        // Compute Covariance manually: (X^T * X) / (n - 1)
        const cov = new Array(w).fill(0).map(() => new Float64Array(w).fill(0));

        for (let i = 0; i < w; i++) {
            for (let j = i; j < w; j++) { // Symmetric
                let sum = 0;
                for (let r = 0; r < h; r++) {
                    sum += centered[r][i] * centered[r][j];
                }
                const val = sum / (h - 1);
                cov[i][j] = val;
                cov[j][i] = val;
            }
        }

        // Eigendecomposition of Covariance
        const svdCov = new SVD(cov); // Covariance is symmetric positive semi-definite. SVD matches Eigen.
        // U equal V. S are eigenvalues.

        const eigenVectors = svdCov.V; // Columns are eigenvectors.
        // ml-matrix SVD sorts by singular values descending? Yes.

        // Select k
        const projectionMatrix = eigenVectors.subMatrix(0, w - 1, 0, k - 1);

        // Project: data * projection
        // Manual Mult: (h x w) * (w x k) -> (h x k)
        // Then Reconstruct: result * projection^T -> (h x k) * (k x w) -> (h x w)

        // Optimization: combine operations?
        // X_hat = X * (P * P^T)
        // P * P^T is (w x w) projection matrix.
        // Let M = P * P^T.
        // X_hat = X * M.

        const M = projectionMatrix.mmul(projectionMatrix.transpose());

        // Apply M to centered data
        const reconstructed = [];
        for (let r = 0; r < h; r++) {
            const row = new Float64Array(w);
            for (let c = 0; c < w; c++) {
                let sum = 0;
                for (let l = 0; l < w; l++) {
                    sum += centered[r][l] * M.get(l, c);
                }
                row[c] = sum + mean[c];
            }
            reconstructed.push(row);
        }

        // Return intermediate data if requested for "How It Works"
        const result = {
            reconstructed: reconstructed,
            covariance: k <= 20 ? cov : [], // Only return if small-ish or requested? Let's return header.
            // Actually returning full 1000x1000 matrix is bad for UI.
            // The original app showed the matrix. 
            // We'll return a subset or the top corner for display if large.
            covarianceSample: cov.slice(0, 5).map(row => row.slice(0, 5)),
            eigenValues: svdCov.diagonal.slice(0, 10), // Top 10
            eigenVectors: eigenVectors.subMatrix(0, 4, 0, 4).to2DArray() // Top 5x5 sample
        };
        return result;
    };

    const rRec = processChannel(r);
    const gRec = processChannel(g);
    const bRec = processChannel(b);

    // Recombine
    const newData = new Uint8ClampedArray(width * height * 4);
    for (let i = 0; i < width * height; i++) {
        const row = Math.floor(i / width);
        const col = i % width;
        // rRec.reconstructed is the data if we changed the return type.
        // Wait, I need to refactor processChannel to return object.

        newData[i * 4] = rRec.reconstructed[row][col];
        newData[i * 4 + 1] = gRec.reconstructed[row][col];
        newData[i * 4 + 2] = bRec.reconstructed[row][col];
        newData[i * 4 + 3] = 255;
    }

    // Construct analysis data if needed
    const analysis = {
        red: { cov: rRec.covarianceSample, eigVals: rRec.eigenValues, eigVecs: rRec.eigenVectors },
        green: { cov: gRec.covarianceSample, eigVals: gRec.eigenValues, eigVecs: gRec.eigenVectors },
        blue: { cov: bRec.covarianceSample, eigVals: bRec.eigenValues, eigVecs: bRec.eigenVectors }
    };

    return { newData, analysis };
}
