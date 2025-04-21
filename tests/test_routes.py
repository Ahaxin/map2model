import unittest
from app.main import create_app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_osm_route_missing_place(self):
        response = self.app.get('/fetch/osm')
        self.assertEqual(response.status_code, 400)

    def test_terrain_route_missing_bbox(self):
        response = self.app.get('/fetch/terrain')
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
