import open3d as o3d
import numpy as np

# Load .obj files# Load .obj files
mesh1 = o3d.io.read_triangle_mesh("output/cat_view_1/mesh.obj")
mesh2 = o3d.io.read_triangle_mesh("output/cat_view_2/mesh.obj")

# Preprocess
mesh1.remove_duplicated_vertices()
mesh2.remove_duplicated_vertices()

# Convert meshes to point clouds
pcd1 = mesh1.sample_points_uniformly(number_of_points=10000)
pcd2 = mesh2.sample_points_uniformly(number_of_points=10000)

# Initial alignment (PCA)
pcd1_center = pcd1.get_center()
pcd2_center = pcd2.get_center()
pcd1.translate(-pcd1_center)
pcd2.translate(-pcd2_center)

print("pre estimate normals")
# Estimate normals - since the point clouds are sampled from the mesh, normals are not available 
# more generally no assumption can be made that normals from each .obj files are calculated in the same way
pcd1.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
pcd2.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.1, max_nn=30))
print("post estimate normals")

# Fine registration (ICP)
reg_p2p = o3d.pipelines.registration.registration_icp(
    pcd1, pcd2, 0.05, np.identity(4),
    o3d.pipelines.registration.TransformationEstimationPointToPoint())

# Apply transformation
pcd1.transform(reg_p2p.transformation)

# Merge point clouds
pcd_combined = pcd1 + pcd2

# Ensure consistent normals
pcd_combined.orient_normals_consistent_tangent_plane(100)

# Surface reconstruction
merged_mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pcd_combined, depth=9)

# Post-processing: remove low density vertices
vertices_to_remove = densities < np.quantile(densities, 0.01)
merged_mesh.remove_vertices_by_mask(vertices_to_remove)

# Save result
o3d.io.write_triangle_mesh("merged_model.obj", merged_mesh)
