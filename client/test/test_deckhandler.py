import sys
import os
import json
import unittest
import shutil
import tempfile

if __name__ == '__main__':
        sys.path.append('././')

from client.main.deckhandler import DeckHandler
from testsuite import TestUtils


class TestDeckHandler(unittest.TestCase):
    """ Testclass for class Deck from client.main.deck """


    @classmethod
    def setUpClass(cls):        
        
        cls.test_files_dict = {
            'valide': """
            {
                "deckname": "Test",
                "filename": "2018-07-07-000816_Leo_4.json",
                "creatorname": "Tester",
                "maxAttrPoints": "4", 
                "minions": {"a": {"minionName": "a",
                "attack": "1", "hp": "1", "skills": ["Attack Face"]}, 
                "s": {"minionName": "s", "attack": "1", "hp": "1", "skills": ["Attack Face"]}}, "id": 1521781072017279922
                
            }   """
            ,

            'invalide': """
            {
                "deckname": "Test",
                "filename": "2018-07-07-000816_Leo_4.json",
                "creatorname": "Leo",
                "maxAttrPoints": "4", 
                "minions": {"a": {"minionName": "a",
                "attack": "1", "hp": "1", "skills": ["Attack Face"]}, 
                "s": {"minionName": "s", "attack": "1", "hp": "1", "skills": ["Attack Face"]}}, "id": 1521781072017279922
                
              """ ,

            'match': """
            {
                "deckname": "Test",
                "filename": "2018-07-07-000816_Leo_4.json",
                "creatorname": "Leo",
                "maxAttrPoints": "4", 
                "minions": {"a": {"minionName": "a",
                "attack": "1", "hp": "1", "skills": ["Attack Face"]}, 
                "s": {"minionName": "s", "attack": "1", "hp": "1", "skills": ["Attack Face"]}}, "id": 1521781072017279922
                
            }   """ ,

            'mismatch': """
            {
                "deckname": "Test",
                "filename": "2018-07-07-000816_Leo_4.json",
                "creatorname": "",
                "maxAttrPoints": "4", 
                "minions": {"a": {"minionName": "a",
                "attack": "1", "hp": "1", "skills": ["Attack Face"]}, 
                "s": {"minionName": "s", "attack": "1", "hp": "1", "skills": ["Attack Face"]}}, "id": 1521781072017279922
                
            }   """ ,
            'empty': ""
        }

        cls.new_dir = str()
        cls.testdict = json.loads(cls.test_files_dict['valide'])

    def setUp(self):
        
        new_dir = tempfile.mkdtemp(prefix="DeckHandlerTest")
        self.new_dir = new_dir
        for filename, content in self.test_files_dict.items():
            
            with open(os.path.join(new_dir, filename), 'w+') as f:
                f.write(content)

    def tearDown(self):
        shutil.rmtree(self.new_dir)

    @classmethod
    def tearDownClass(cls):
        pass
    
    ####################### TESTS #############################

    def test_list_decks(self):
        """ test for method: get_decks"""
        
        handler = DeckHandler(self.new_dir)
        user_list = ["Leo"]
        for user in user_list:
            TestUtils.blockPrint()
            dictList = handler.list_decks(user)
            TestUtils.enablePrint()
            self.assertEqual(1, len(dictList))
    
    def test_create_deck(self):
        
        handler = DeckHandler(self.new_dir)
        deck = handler.create_deck('TestUser', self.testdict)
        testDict = self.testdict
        testDict.update({'creatorname': "TestUser"})
        testDict.update({'id': deck['id']})

        self.assertIsNotNone(deck)
        with open(os.path.join(self.new_dir,  deck['id'])) as f:
            deckDict = json.load(f)
            self.assertDictEqual(self.testdict, deckDict)

    def test_get_deck(self):

        handler = DeckHandler(self.new_dir)
        user_id = "TestUser"
        deck_id = "valide"
        deck = handler.get_deck(user_id, deck_id)
        testDict = self.testdict
        testDict.update({'creatorname': deck['creatorname']})
        testDict.update({'id': deck['id']})
        self.assertIsNotNone(deck)
        self.assertEqual(self.testdict, deck)

    def test_get_deck_no_valid_id(self):

        handler = DeckHandler(self.new_dir)
        user_id = "TestUser"
        deck_id = "xyz"
        deck = handler.get_deck(user_id, deck_id)
        self.assertEqual({}, deck)

    def test_delete_deck(self):

        handler = DeckHandler(self.new_dir)
        self.assertEqual(len(self.test_files_dict), len(os.listdir(self.new_dir)))
        userId = "Tester"
        deckId = 'valide'
        response = handler.delete_deck(userId, deckId)
        self.assertEqual(len(self.test_files_dict)-1, len(os.listdir(self.new_dir)))
        self.assertTrue(response)

    def test_delete_deck_nonExistingDeck(self):

        handler = DeckHandler(self.new_dir)
        self.assertEqual(len(self.test_files_dict), len(os.listdir(self.new_dir)))
        userId = ""
        deckId = 'xyz' # xyz is not the id
        response = handler.delete_deck(userId, deckId)
        self.assertEqual(len(self.test_files_dict), len(os.listdir(self.new_dir)))
        self.assertFalse(response)


            

if __name__ == '__main__':
        unittest.main()
        
