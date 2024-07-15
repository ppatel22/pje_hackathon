# Drone Vision
Drone vision project for PJE hackathon.
3D Point Cloud Estimation of Surfaces Using Drones

## Steps to Installation 
Create a python venv and install the packages needed via ```pip install -r requirements.txt```.

## Problem Statement
- From peril to precision: Transitioning from high-risk manned reconnaissance to safer autonomous data collection
- Elevating perception: From flat footage to dimensional data for machine navigation
- Sky high costs: Satellite & aerial imagery are expensive, drones are not.

## Solution
3D Reconstruction via Point Cloud Estimation
Photogrammetry tries to reverse the depth info loss incurred by photography
Multi-step approach to reconstruct scenes from images/videos
- Feature extraction, Image matching, Features matching, Structure from motion, Depth maps, Meshing, Texturing, Localization

## Demo 
https://github.com/user-attachments/assets/f6d3a4db-dec6-49ab-b7b0-027355f785c6

## Problems In The Field
Accounting for change
→ real world: would be useful to track “change” overtime for dynamic updating
→ solution: looking at the differential in successive runs / realtime updates (for moving objects)

Transmission of high-quality data with a singular drone
→ real world: multiple parallel drones recording & sending 1 image/x frames
→ solution: perform sparse-view 3D image reconstruction (using neural networks)


## Appendix: Technical Details
- `generate_mesh.py` uses AliceVision’s Meshroom photogrammetry library to generate a 3D mesh from a video.
- Pipeline explanation: https://alicevision.org/#photogrammetry/natural_feature_extraction
    - SIFT Feature extraction: difference of Gaussians computed at different scales, extrema gathered as keypoints
    - For each keypoint, create a histogram of gradients for the surrounding points
    - ‘Structure from Motion’ - Makes tracks with the corresponding key points via RANSAC
    - Depth estimation - Semi-Global Matching (SGM)
    - Meshing - 3D Delaunay tetrahedralization
