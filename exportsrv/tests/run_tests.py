
import unittest
import sys

if __name__ == '__main__':
    suite = unittest.TestLoader().discover('unittests')
    results = unittest.TextTestRunner(verbosity=3).run(suite)
    if results.errors or results.failures:
        sys.exit(1)