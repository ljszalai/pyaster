import unittest
import random_util


class MyTestCase(unittest.TestCase):
    def test_visualize_results(self):
        column_width = 20
        print("Generated id:".rjust(column_width, ' ') + random_util.generate_id())
        print("Generated uuid:".rjust(column_width, ' ') + random_util.generate_uuid())
        print("Generated token:".rjust(column_width, ' ') + random_util.generate_token())


if __name__ == '__main__':
    unittest.main()
