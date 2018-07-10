import sys
import unittest


if __name__ == '__main__':
    # Run only the tests in the specified classes

    sys.path.append('././')
    from client.test.test_deck import TestDeck
    from common.test.test_browsedeck import TestBrowseDecks
    from client.test.test_deckhandler import TestDeckHandler

    # Add TestClasses in this list
    test_classes_to_run = [TestDeck, TestBrowseDecks, TestDeckHandler]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)

class TestUtils:
    """Class with static Methods for Unittesting"""

    # Disable print
    @staticmethod
    def blockPrint():
        sys.stdout = None 

    # Restore print
    @staticmethod
    def enablePrint():
        sys.stdout = sys.__stdout__

