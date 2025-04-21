import os
import tempfile
import geopandas as gpd
import osmnx as ox
import elevation

class MapFetcher:
    def __init__(self, download_dir="static/models"):
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    def fetch_osm_data(self, place_name: str, tags=None):
        print(f"[+] Fetching OSM data for: {place_name}")
        if tags is None:
            tags = {"building": True}

        try:
            gdf = ox.geometries_from_place(place_name, tags)
            file_path = os.path.join(self.download_dir, f"{place_name.replace(' ', '_')}_osm.geojson")
            gdf.to_file(file_path, driver="GeoJSON")
            return file_path
        except Exception as e:
            print("[-] Error fetching OSM:", e)
            return None

    def fetch_srtm_elevation(self, bbox):
        tempdir = tempfile.mkdtemp()
        file_path = os.path.join(self.download_dir, "elevation.tif")

        try:
            elevation.clip(bounds=bbox, output=file_path)
            return file_path
        except Exception as e:
            print("[-] Error downloading elevation:", e)
            return None
