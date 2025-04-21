from flask import Blueprint, request, jsonify
from app.services.map_fetcher import MapFetcher

api = Blueprint("api", __name__)
fetcher = MapFetcher()

@api.route("/fetch/osm", methods=["GET"])
def fetch_osm():
    place = request.args.get("place")
    if not place:
        return jsonify({"error": "Missing place parameter"}), 400

    path = fetcher.fetch_osm_data(place)
    return jsonify({"file": path if path else "Failed to fetch"})

@api.route("/fetch/terrain", methods=["GET"])
def fetch_terrain():
    try:
        bbox = request.args.get("bbox")
        minlon, minlat, maxlon, maxlat = map(float, bbox.split(","))
        path = fetcher.fetch_srtm_elevation((minlon, minlat, maxlon, maxlat))
        return jsonify({"file": path if path else "Failed to fetch"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
