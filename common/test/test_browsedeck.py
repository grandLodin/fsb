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




class TestBrowseDecks(unittest.TestCase):
    """ Testclass for class BrowseDecks from common.main.browsedeck """

    # Disable print
    @staticmethod
    def blockPrint():
        sys.stdout = None 

    # Restore print
    @staticmethod
    def enablePrint():
        sys.stdout = sys.__stdout__

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
        self.deck.mMinionList = []
        self.deck.mDeckDict = None

        self.player.mPlayerName = "TestPlayer"

        self.minion.mMinionName = "testminion"
        self.minion.mAttackPoints = 1
        self.minion.mHealthPoints = 1
        self.minion.mSkills = [self.skill]

        self.skill.mSkillName = "Taunt"

        self.testdictionary = {"deckname": "test_", "filename": "test.json", "Creatorname": "Tester_", "maxAttrPoints": "4", "minions": {"testminion_": {"minionName": "testminion_", "attack": "2", "hp": "2", "skills": ["Attack Face"]}}}

    def tearDown(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass
    
    ######################## TESTS #############################
    
    # createDeckDialog not tested. already covered by other tests

    @patch("client.main.deck.Deck.timenow", return_value = MockTime)
    def test_autoFilename(self, pTesttime):
        filename = self.deck.autoFilename
        self.assertEqual(filename, "0-1-2-345_Tester_0.json")

    def test_setMaxAttributePoint(self):
        """ test for method: setMaxAttributePoint"""

        with patch('client.main.deck.Deck.getInput_setMaxAttributePoints', return_value = 2):
            self.blockPrint()
            self.deck.setMaxAttributePoints()
            self.enablePrint()
        self.assertEqual(self.deck.mMaxAttributePoints , 2)

        self.deck.mMaxAttributePoints = 0
        
        inputs = [0, -1, ""]
        for i in inputs:
            try: 
                with patch('client.main.deck.Deck.getInput_setMaxAttributePoints', return_value=i):
                    self.blockPrint()
                    self.deck.setMaxAttributePoints()
                    self.enablePrint()
            except RecursionError:
                self.assertEqual(self.deck.mMaxAttributePoints , 0)

    # @patch('common.main.minion.Minion.getInput_setUniqueName', return_value = "" )
    # @patch('common.main.minion.Minion.getInput_setHealthPoints', return_value = 1 )
    # @patch('common.main.minion.Minion.getInput_setAttackPoints', return_value = 1 )
    # @patch('pick.Picker.start', return_value = ("Attack Face", 0) )
    def test_createMinion(self):#, mock_name, mock_hp, mock_attack, mock_pick):
        """ test for method: createMinion"""

        self.deck.mMinionList = []

        with patch('common.main.minion.Minion.getInput_setUniqueName', return_value=""):
            with patch('common.main.minion.Minion.getInput_setHealthPoints', return_value=1):
                with patch('common.main.minion.Minion.getInput_setAttackPoints', return_value=1):
                    with patch('pick.Picker.start', return_value = ("Attack Face", 0)):
                                self.deck.createMinions(0)
                                self.assertListEqual(self.deck.mMinionList, [])

                                self.blockPrint()
                                self.deck.createMinions(2)
                                self.enablePrint()
                                self.assertEqual(len(self.deck.mMinionList), 1 )

                                try: 
                                    self.blockPrint()
                                    self.deck.createMinions(3)
                                    self.enablePrint()
                                except RecursionError:  # because unable to set unique name
                                    self.assertEqual(len(self.deck.mMinionList), 1)

    def test_chooseDeckName(self):
        """ test for method: chooseDeckName"""

        inputs = ["Test Deck", 0, True, 2.455, [] ]
        for i in inputs:
            with patch('client.main.deck.Deck.getInput_chooseDeckName', return_value = i):
                self.deck.chooseDeckName()
            self.assertEqual(self.deck.mDeckName, i)

    def test_createDictionary(self):
        """ tests method: createDictionary"""

        self.deck.mMinionList = [self.minion]

        deckDict = self.deck.createDictionary()
        self.assertIsNotNone(deckDict)
        self.assertEqual(deckDict['deckname'], "test" )
        self.assertIsInstance(deckDict['filename'], str)
        self.assertEqual(deckDict['Creatorname'], "Tester" )
        self.assertEqual(deckDict['maxAttrPoints'], "0")
        self.assertEqual(deckDict['minions'], {"testminion": {"minionName": "testminion", "attack": "1", "hp": "1", "skills": ["Taunt"]}} )

    def test_parseDeck(self):
        """ tests method: parseDeck"""

        deckDict = {"deckname": "test_", "filename": "test.json_", "Creatorname": "Tester_", "maxAttrPoints": "4", "minions": {"testminion_": {"minionName": "testminion_", "attack": "2", "hp": "2", "skills": ["Attack Face"]}}}
        self.deck.parseDeck(deckDict, self.player.mPlayerName)

        self.assertEqual(self.deck.mDeckName, "test_")
        self.assertEqual(self.deck.mFilename, "test.json_")
        self.assertEqual(self.deck.mCreatorname, "Tester_")
        self.assertEqual(self.deck.mMaxAttributePoints, 4)
        self.assertEqual(len(self.deck.mMinionList), 1)
        self.assertEqual(self.deck.mDeckDict, deckDict)

    #selectDeck not tested. Called method will be tested in test_browsedeck

    def test_findMinionsInDeck(self):
        """tests method: findMinionsInDeck"""

        deckDict = {"deckname": "test_", "filename": "test.json_", "Creatorname": "Tester_", "maxAttrPoints": "4", "minions": {"testminion_": {"minionName": "testminion_", "attack": "2", "hp": "2", "skills": ["Attack Face"]}}}
        playername = "Tester"

        minionlist = self.deck.findMinionsInDeck(deckDict, playername)

        self.assertIsNotNone(minionlist)
        self.assertEqual(len(minionlist), 1)

    def test_saveDeck(self):
        """tests method: saveDeck"""

        deckDict = {"deckname": "test_", "filename": "test.json", "Creatorname": "Tester_",
                    "maxAttrPoints": "4", "minions": {"testminion_": {"minionName": "testminion_", "attack": "2",
                                                                      "hp": "2", "skills": ["Attack Face"]}}}
        filename = "./decks/test.json"

        try:
            self.deck.saveDeck(self.testdictionary)
            with open(filename) as f:
                    content = json.load(f)
        finally:
            os.remove(filename)
        self.assertEqual(content, deckDict)


if __name__ == '__main__':
        unittest.main()
