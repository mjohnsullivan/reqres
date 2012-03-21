"""
Runs all tests
"""

import unittest

# -- Import the test modules
from tests.test_request import TestRequest

# -- Create test suites for each test case module
test_request_suite = unittest.TestLoader().loadTestsFromTestCase(TestRequest)

# -- Create a single all-encompassing test suite
test_suite = unittest.TestSuite(
    (test_request_suite,)
)

# -- Set the log level
# logging.basicConfig(level = logging.DEBUG)

# -- Run the tests
unittest.TextTestRunner(verbosity = 2).run(test_suite)
