import unittest
import doctest
import drawzero.utils.pt

# All tests for Pt class are in doc string
# So we just run doctests
class RunTestsFromDocTests(unittest.TestCase):
    def test_doctests(self):
        testSuite = doctest.DocTestSuite(drawzero.utils.pt)
        unittest.TextTestRunner().run(testSuite)


################################################################################

if __name__ == "__main__":
    unittest.main()
