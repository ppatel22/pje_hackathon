# Drone Vision
Drone vision project for PJE hackathon.

## Steps to Installation 
Create a python venv and install the packages needed via ```pip install -r requirements.txt```.

## Problem Statement
From peril to precision: Transitioning from high-risk manned reconnaissance to safer autonomous data collection
Elevating perception: From flat footage to dimensional data for machine navigation
Sky high costs: Satellite & aerial imagery are expensive, drones are not.

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

