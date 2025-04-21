import unittest
import os
from app.services.model_generator import ModelGenerator

class TestModelGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = ModelGenerator(output_dir="static/test_output")
        os.makedirs("static/test_output", exist_ok=True)

    def test_generate_osm_model(self):
        geojson_path = "static/test_models/Monaco_osm.geojson"
        if not os.path.exists(geojson_path):
            self.skipTest(f"Test file {geojson_path} does not exist")

        result = self.generator.generate_3d_model_from_osm(geojson_path, height=15)
        self.assertTrue(result and result.endswith(".stl"), "Failed to generate OSM model")

    def test_generate_terrain_model(self):
        tiff_path = "static/test_models/elevation.tif"
        if not os.path.exists(tiff_path):
            self.skipTest(f"Test file {tiff_path} does not exist")

        result = self.generator.generate_3d_model_from_elevation(tiff_path, z_scale=2.0, skip=3)
        self.assertTrue(result and result.endswith(".stl"), "Failed to generate terrain model")

if __name__ == '__main__':
    unittest.main()
