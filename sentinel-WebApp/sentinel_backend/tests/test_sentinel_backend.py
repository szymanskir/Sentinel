import unittest

import sentinel_backend


class Sentinel_backendTestCase(unittest.TestCase):

    def setUp(self):
        self.app = sentinel_backend.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to Sentinel', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
