import unittest
from app.main import create_app

class TestMainApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_root_response(self):
        response = self.app.get('/')
        self.assertIn(response.status_code, [404, 200])  # Default route behavior

if __name__ == '__main__':
    unittest.main()
