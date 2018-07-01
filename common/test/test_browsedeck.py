import sys
import unittest
from unittest.mock import patch
if __name__ == '__main__':
        sys.path.append('././')
from testsuite import TestUtils
from common.main.browsedecks import BrowseDecks
from client.main.deck import Deck

class TestBrowseDecks(unittest.TestCase):
    """ Testclass for class BrowseDecks from common.main.browsedeck """

    @classmethod
    def setUpClass(cls):        
        
        cls.deck = Deck()
        cls.browsedeck = BrowseDecks(True)
        cls.selectdeck = BrowseDecks(False)
        cls.testdeck = {"deckname": "test_", "filename": "test.json", "Creatorname": "Tester_", "maxAttrPoints": "4", "minions": {"testminion_": {"minionName": "testminion_", "attack": "2", "hp": "2", "skills": ["Attack Face"]}}}
    
    def setUp(self):
        self.browsedeck.mPath = "./decks/testdecks/"
        self.selectdeck.mPath = "./decks/testdecks/"

    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    ######################## TESTS #############################

    @patch("common.main.browsedecks.BrowseDecks.getInput_pickDeck", return_value= ("testdeck",["testdeck.json"] , 0))
    def test_browseDecksInBrowseMode(self, pPick):
        """ test for method: browseDecks if Class is in BrowseMode"""

        self.assertTrue(self.browsedeck.mIsinBrowseMode)
        self.assertFalse(self.browsedeck.mIsDeckSelected)

        with patch("common.main.browsedecks.BrowseDecks.getInput_YesOrNo", return_value="n"):
            TestUtils.blockPrint()
            self.browsedeck.browseDecks()
            TestUtils.enablePrint()
        self.assertTrue(self.browsedeck.mIsDeckSelected)

        with patch("common.main.browsedecks.BrowseDecks.getInput_YesOrNo", return_value="y"):
            self.browsedeck.mIsDeckSelected = False
            TestUtils.blockPrint()
            self.assertRaises(RecursionError, self.browsedeck.browseDecks)
            TestUtils.enablePrint()

    @patch("common.main.browsedecks.BrowseDecks.getInput_pickDeck", return_value= ("testdeck",["testdeck.json"] , 0))
    def test_browseDecksNotInBrowseMode(self, pPick):
        """ test for method: browseDecks if Class is in BrowseMode"""

        self.assertFalse(self.selectdeck.mIsinBrowseMode)
        self.assertFalse(self.selectdeck.mIsDeckSelected)

        with patch("common.main.browsedecks.BrowseDecks.getInput_YesOrNo", return_value="y"):
            TestUtils.blockPrint()
            self.selectdeck.browseDecks()
            TestUtils.enablePrint()
        self.assertTrue(self.selectdeck.mIsDeckSelected)
        self.assertEqual(self.selectdeck.mDeckName, "testdeck")
        self.assertEqual(self.selectdeck.mDeck, self.testdeck )

        with patch("common.main.browsedecks.BrowseDecks.getInput_YesOrNo", return_value="n"):
            self.selectdeck.mIsDeckSelected = False
            TestUtils.blockPrint()
            self.assertRaises(RecursionError, self.selectdeck.browseDecks)
            TestUtils.enablePrint()

if __name__ == '__main__':
        unittest.main()
