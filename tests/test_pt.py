import unittest
import doctest
import drawzero.utils.pt


class RunTestsFromDocTests(unittest.TestCase):
    def test_doctests(self):
        testSuite = doctest.DocTestSuite(drawzero.utils.pt)
        unittest.TextTestRunner().run(testSuite)


################################################################################

if __name__ == "__main__":
    unittest.main()
