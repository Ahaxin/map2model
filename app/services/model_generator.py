# Create a starter model_generator.py that supports basic conversion structure
import os
import geopandas as gpd
import numpy as np
import trimesh
from shapely.geometry import Polygon, MultiPolygon
import rasterio
from rasterio.enums import Resampling
from matplotlib import cm
from scipy.ndimage import gaussian_filter
import trimesh


class ModelGenerator:
    def __init__(self, output_dir="static/models"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_3d_model_from_osm(self, geojson_path, height=20):
        
        # Converts building footprints from a GeoJSON into a simple extruded 3D model.
        
        try:
            gdf = gpd.read_file(geojson_path)
            geometries = gdf.geometry

            meshes = []
            for geom in geometries:
                if isinstance(geom, (Polygon, MultiPolygon)):
                    mesh = self._extrude_polygon(geom, height)
                    if mesh:
                        meshes.append(mesh)

            if not meshes:
                print("[-] No valid geometries to extrude.")
                return None

            combined = trimesh.util.concatenate(meshes)
            model_path = os.path.join(self.output_dir, "osm_model.stl")
            combined.export(model_path)
            return model_path

        except Exception as e:
            print("[-] Error generating 3D model from OSM:", e)
            return None

    def _extrude_polygon(self, geom, height):
        
        # Extrudes a shapely Polygon into a 3D mesh using trimesh.
        
        try:
            if geom.is_empty:
                return None
            if isinstance(geom, MultiPolygon):
                parts = [trimesh.creation.extrude_polygon(p, height) for p in geom.geoms]
                return trimesh.util.concatenate(parts)
            else:
                return trimesh.creation.extrude_polygon(geom, height)
        except Exception as e:
            print("[-] Error extruding polygon:", e)
            return None

    def generate_3d_model_from_elevation(self, tiff_path, z_scale=0.0001, skip=1, smooth_sigma=10):
        """
        Converts a GeoTIFF elevation file to a 3D terrain STL.
        z_scale: scales vertical exaggeration
        skip: step size to reduce mesh complexity
        smooth_sigma: controls level of terrain smoothing
        """
        # test area 121.517487,38.935378,121.941833,39.080507
        try:
            with rasterio.open(tiff_path) as dataset:
                elevation = dataset.read(1, resampling=Resampling.bilinear)
                elevation = np.nan_to_num(elevation)

                # Downsample to reduce complexity
                # elevation = elevation[::skip, ::skip]

                # Smooth the terrain to remove spikes
                elevation = gaussian_filter(elevation, sigma=smooth_sigma)
                #elevation = np.clip(elevation, np.percentile(elevation, 1), np.percentile(elevation, 99))

                nrows, ncols = elevation.shape

                # Generate vertex grid
                x, y = np.meshgrid(np.arange(ncols), np.arange(nrows))
                z = elevation * z_scale

                # Flatten arrays for mesh
                vertices = np.column_stack((x.flatten(), y.flatten(), z.flatten()))

                # Generate triangular faces
                faces = []
                for row in range(nrows - 1):
                    for col in range(ncols - 1):
                        a = row * ncols + col
                        b = a + 1
                        c = a + ncols
                        d = c + 1
                        faces.append([a, c, b])
                        faces.append([b, c, d])

                # Create and export the mesh
                mesh = trimesh.Trimesh(vertices=vertices, faces=np.array(faces))
                model_path = os.path.join(self.output_dir, "terrain_model.stl")
                mesh.export(model_path)
                return model_path

        except Exception as e:
            print("[-] Error generating terrain model:", e)
            return None