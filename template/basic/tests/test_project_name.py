#!/usr/bin/env python3
import unittest
import sys
import os
if "<PROJECT_NAME>" not in sys.modules:
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    from <PROJECT_NAME> import *


class Test<PROJECT_CLASS>(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        return super().tearDown()

    def test_sample(self):
        pass

    pass


if __name__ == "__main__":
    unittest.main()
    pass
