
import os
import geopandas as gpd
import requests
from shapely.geometry import shape
from app.config import OPENTOPO_API_KEY

class MapFetcher:
    def __init__(self, download_dir="static/models"):
        self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

    def fetch_osm_data(self, bbox):
        """
        Downloads building data within a bounding box using Overpass API.
        bbox = (minlon, minlat, maxlon, maxlat)
        """
        minlon, minlat, maxlon, maxlat = bbox
        print(f"[+] Fetching OSM data for BBOX: {bbox}")

        query = f"""
        [out:json][timeout:25];
        (
          way["building"]({minlat},{minlon},{maxlat},{maxlon});
          relation["building"]({minlat},{minlon},{maxlat},{maxlon});
        );
        out body;
        >;
        out skel qt;
        """

        try:
            response = requests.get(
                "https://overpass-api.de/api/interpreter",
                params={"data": query}
            )
            data = response.json()

            # Convert to GeoDataFrame
            from osm2geojson import json2geojson
            geojson_data = json2geojson(data)
            gdf = gpd.GeoDataFrame.from_features(geojson_data["features"])

            # Save it
            file_path = os.path.join(self.download_dir, f"osm_bbox.geojson")
            gdf.to_file(file_path, driver="GeoJSON")
            return file_path
        except Exception as e:
            print("[-] Error fetching Overpass data:", e)
            return None

    def fetch_srtm_elevation(self, bbox):
        minlon, minlat, maxlon, maxlat = bbox
        api_url = "https://portal.opentopography.org/API/globaldem"
        params = {
            "demtype": "SRTMGL1",
            "south": minlat,
            "north": maxlat,
            "west": minlon,
            "east": maxlon,
            "outputFormat": "GTiff",
            "API_Key": OPENTOPO_API_KEY
        }

        try:
            response = requests.get(api_url, params=params, stream=True)
            if response.status_code == 200:
                file_path = os.path.join(self.download_dir, "elevation.tif")
                with open(file_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return file_path
            else:
                print(f"[-] OpenTopography API error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print("[-] Error fetching elevation:", e)
            return None
