# pje_hackathon
Drone project for PJE hackathon.

## Video to Mesh
- `generate_mesh.py` uses AliceVision's Meshroom photogrammetry library to generate a 3D mesh from a video.
- Pipeline explanation: https://alicevision.org/#photogrammetry/natural_feature_extraction
    - SIFT Feature extraction: difference of Gaussians computed at different scales, extrema gathered as keypoints
    - For each keypoint, create a histogram of gradients for the surrounding points
    - 'Structure from Motion' - Makes tracks with the corresponding key points via RANSAC