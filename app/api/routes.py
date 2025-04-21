from flask import Blueprint, request, jsonify
from app.services.map_fetcher import MapFetcher
from app.services.model_generator import ModelGenerator
import os

api = Blueprint("api", __name__)
fetcher = MapFetcher()
generator = ModelGenerator()

@api.route("/fetch/osm", methods=["GET"])
def fetch_osm():
    bbox_str = request.args.get("bbox")
    if not bbox_str:
        return jsonify({"error": "Missing bbox parameter"}), 400

    try:
        minlon, minlat, maxlon, maxlat = map(float, bbox_str.split(","))
    except:
        return jsonify({"error": "Invalid bbox format"}), 400

    path = fetcher.fetch_osm_data((minlon, minlat, maxlon, maxlat))
    return jsonify({"file": path if path else "Failed to fetch"})

@api.route("/fetch/terrain", methods=["GET"])
def fetch_terrain():
    try:
        bbox = request.args.get("bbox")  # Format: "minlon,minlat,maxlon,maxlat"
        minlon, minlat, maxlon, maxlat = map(float, bbox.split(","))
        path = fetcher.fetch_srtm_elevation((minlon, minlat, maxlon, maxlat))
        return jsonify({"file": path if path else "Failed to fetch"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api.route("/generate/osm-model", methods=["POST"])
def generate_osm_model():
    data = request.get_json()
    geojson_path = data.get("geojson_path")
    height = float(data.get("height", 20))

    if not geojson_path or not os.path.exists(geojson_path):
        return jsonify({"error": "Invalid or missing geojson_path"}), 400

    result = generator.generate_3d_model_from_osm(geojson_path, height)
    return jsonify({"file": result if result else "Failed to generate"})


@api.route("/generate/terrain-model", methods=["POST"])
def generate_terrain_model():
    data = request.get_json()
    tiff_path = data.get("tiff_path")
    z_scale = float(data.get("z_scale", 1.0))
    skip = int(data.get("skip", 1))

    if not tiff_path or not os.path.exists(tiff_path):
        return jsonify({"error": "Invalid or missing tiff_path"}), 400

    result = generator.generate_3d_model_from_elevation(tiff_path, z_scale, skip)
    return jsonify({"file": result if result else "Failed to generate"})
