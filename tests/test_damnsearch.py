"""
Does some stuff
"""
from __future__ import absolute_import
import os
import unittest
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

from damn_index.damnsearch import DAMNSearch

class TestCase(unittest.TestCase):
    """Test case"""
    def test_get_mimetypes_with_count(self):
        """Test get_mimetypes_with_count"""
        search = DAMNSearch()
        
        result = search.get_mimetypes_with_count()


def test_suite():
    """Return a list of tests"""
    return unittest.TestLoader().loadTestsFromTestCase(TestCase)

if __name__ == '__main__':
    #unittest.main()
    unittest.TextTestRunner().run(test_suite())
