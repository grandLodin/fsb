import sys
import os
import json
import unittest
from unittest.mock import patch
if __name__ == '__main__':
        sys.path.append('././')
from client.main.deck import Deck
from common.main.minion import Minion
from common.main.skill import Skill
from server.main.player import Player
from client.test.testutils import MockTime
from testsuite import TestUtils


class TestDeck(unittest.TestCase):
    """ Testclass for class Deck from client.main.deck """

    @classmethod
    def setUpClass(cls):        
        
        cls.deck = Deck()
        cls.player = Player()
        cls.minion = Minion()
        cls.skill = Skill()
    
    def setUp(self):
        self.deck.mLog = ""
        self.deck.mDeckName = "test"
        self.deck.mFilename = "test.json"
        self.deck.mCreatorname = "Tester"
        self.deck.mMaxAttributePoints = 0
        self.deck.mMinionSet = set()
        self.deck.mDeckDict = None

        self.player.mPlayerName = "TestPlayer"

        self.minion.mMinionName = "testminion"
        self.minion.mAttackPoints = 1
        self.minion.mHealthPoints = 1
        self.minion.mSkills = [self.skill]

        self.skill.mSkillName = "Taunt"

        self.testdictionary = {"deckname": "test_", "filename": "test.json", "creatorname": "Tester_", "maxAttrPoints": "4", "minions": {"testminion_": {"minionName": "testminion_", "attack": "2", "hp": "2", "skills": ["Attack Face"]}}}

    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    ######################## TESTS #############################
    
    # createDeckDialog not tested. already covered by other tests

    @patch("client.main.deck.Deck.timenow", return_value=MockTime)
    def test_autoFilename(self, pMocktime):
        """ test for method: autoFilename"""

        filename = self.deck.autoFilename
        self.assertEqual(filename, "1985-01-25-113005_Tester_0.json")

    def test_setMaxAttributePoint(self):
        """ test for method: setMaxAttributePoint"""

        with patch('client.main.deck.Deck.getInput_setMaxAttributePoints', return_value = 2):
            TestUtils.blockPrint()
            self.deck.setMaxAttributePoints()
            TestUtils.enablePrint()
        self.assertEqual(self.deck.mMaxAttributePoints , 2)

        self.deck.mMaxAttributePoints = 0
        
        inputs = [0, -1, ""]
        for i in inputs:
            try: 
                with patch('client.main.deck.Deck.getInput_setMaxAttributePoints', return_value=i):
                    TestUtils.blockPrint()
                    self.deck.setMaxAttributePoints()
                    TestUtils.enablePrint()
            except RecursionError:
                self.assertEqual(self.deck.mMaxAttributePoints, 0)

    def test_createMinion(self):
        """ test for method: createMinion"""

        self.deck.mMinionSet = set()

        with patch('common.main.minion.Minion.getInput_setUniqueName', return_value=""):
            with patch('common.main.minion.Minion.getInput_setHealthPoints', return_value=1):
                with patch('common.main.minion.Minion.getInput_setAttackPoints', return_value=1):
                    with patch('pick.Picker.start', return_value=("Attack Face", 0)):
                                self.deck.createMinions(0)
                                self.assertSetEqual(self.deck.mMinionSet, set())

                                TestUtils.blockPrint()
                                self.deck.createMinions(2)
                                TestUtils.enablePrint()
                                self.assertEqual(len(self.deck.mMinionSet), 1)
                                                                    
    def test_chooseDeckName(self):
        """ test for method: chooseDeckName"""

        inputs = ["Test Deck", 0, True, 2.455, [] ]
        for i in inputs:
            with patch('client.main.deck.Deck.getInput_chooseDeckName', return_value = i):
                self.deck.chooseDeckName()
            self.assertEqual(self.deck.mDeckName, i)

    def test_createDictionary(self):
        """ tests method: createDictionary"""

        self.deck.mMinionSet = [self.minion]

        deckDict = self.deck.createDictionary()
        self.assertIsNotNone(deckDict)
        self.assertEqual(deckDict['deckname'], "test" )
        self.assertIsInstance(deckDict['filename'], str)
        self.assertEqual(deckDict['creatorname'], "Tester" )
        self.assertEqual(deckDict['maxAttrPoints'], "0")
        self.assertEqual(deckDict['minions'], {"testminion": {"minionName": "testminion", "attack": "1", "hp": "1", "skills": ["Taunt"]}} )

    def test_parseDeck(self):
        """ tests method: parseDeck"""

        self.deck.parseDeck(self.testdictionary, self.player.mPlayerName)

        self.assertEqual(self.deck.mDeckName, "test_")
        self.assertEqual(self.deck.mFilename, "test.json")
        self.assertEqual(self.deck.mCreatorname, "Tester_")
        self.assertEqual(self.deck.mMaxAttributePoints, 4)
        self.assertEqual(len(self.deck.mMinionSet), 1)
        self.assertEqual(self.deck.mDeckDict, self.testdictionary)

    #selectDeck not tested. Called method will be tested in test_browsedeck

    def test_findMinionsInDeck(self):
        """tests method: findMinionsInDeck"""

        minionset = self.deck.findMinionsInDeck(self.testdictionary, self.player.mPlayerName)

        self.assertIsNotNone(minionset)
        self.assertEqual(len(minionset), 1)

    def test_saveDeck(self):
        """tests method: saveDeck"""

        deckDict = {"deckname": "test_", "filename": "test.json", "creatorname": "Tester_",
                    "maxAttrPoints": "4", "minions": {"testminion_": {"minionName": "testminion_", "attack": "2",
                                                                      "hp": "2", "skills": ["Attack Face"]}}}
        filename = "./decks/decks/test.json"

        try:
            TestUtils.blockPrint()
            self.deck.saveDeck(self.testdictionary)
            TestUtils.enablePrint()
            with open(filename) as f:
                    content = json.load(f)
        finally:
            os.remove(filename)
        self.assertEqual(content, deckDict)


if __name__ == '__main__':
        unittest.main()
