#!/usr/bin/env python
import unittest

if __name__ == '__main__':
  suite = unittest.TestLoader().discover('unittests')
  unittest.TextTestRunner(verbosity=3).run(suite)