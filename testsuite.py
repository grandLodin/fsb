import sys
sys.path.append('././')
import unittest
from client.test.test_deck import TestDeck

if __name__ == '__main__':
    # Run only the tests in the specified classes

    # Add TestClasses in this list
    test_classes_to_run = [TestDeck]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
