import unittest
from app.services.map_fetcher import MapFetcher

class TestMapFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = MapFetcher(download_dir="static/test_models")

    def test_fetch_osm_data(self):
        file_path = self.fetcher.fetch_osm_data("Monaco")
        self.assertTrue(file_path is None or file_path.endswith("geojson"))

    def test_fetch_srtm_elevation(self):
        bbox = (7.41, 43.72, 7.43, 43.73)  # Area near Monaco
        file_path = self.fetcher.fetch_srtm_elevation(bbox)
        self.assertTrue(file_path is None or file_path.endswith("elevation.tif"))

if __name__ == '__main__':
    unittest.main()
