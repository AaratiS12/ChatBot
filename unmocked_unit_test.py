'''
    This file tests all methods in app.py.
'''

import unittest
import app
import unittest.mock as mock
from app import bot_response_api
import json  

KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_LENGTH = "length"
KEY_FIRST_WORD = "first_word"
KEY_SECOND_WORD = "second_word"

class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_help = [
            {
                KEY_INPUT: "!! help",
                KEY_EXPECTED: "Type either: \n1)!! translate/funtranslate {text}\n2)!! tamil-translate {text}\n3)!! random-fact\n4)!! text-to-binary {text}\n5)!! help\n6)!! about"
            },]
        self.success_test_about_me = [        
            {
                KEY_INPUT: "!! about me",
                KEY_EXPECTED: "I am a bot, I will respond to messages that start with !!"
            },]
        self.success_test_tamil_translate = [  
            {
                KEY_INPUT: "!! tamil-translate coconut",
                KEY_EXPECTED: "தேங்காய்"
            },]
        self.failure_test_tamil_translate = [      
            {
                KEY_INPUT: "! tamil-translate coconut",
                KEY_EXPECTED: "Command not found"
            },
        ]
        self.error_tamil_translate_test_params = [
            {
                KEY_INPUT: "!! tamil-translate",
                KEY_EXPECTED: "Error: text not given" 
            },]
        
        self.failure_test_text_to_binary = [
            {
                KEY_INPUT: "!! text-to-binary",
                KEY_EXPECTED: "Error: text not given" },
            ]  
            
        self.error_funtranslate_test_params = [
            {
                KEY_INPUT: "!! funtranslate",
                KEY_EXPECTED: "Error: text not given" 
            },
            ] 
            
             
    #UNMOCKED TESTS
    def test_help_success(self):
        for test in self.success_test_help:
            helps = app.bot_response_api(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(helps, expected)
            
    def test_about_me_success(self):
        for test in self.success_test_about_me:
            about_me = app.bot_response_api(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(about_me, expected)
            
    def test_tamil_translate_success(self):
        for test in self.success_test_tamil_translate:
            tamil_translate = app.bot_response_api(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(tamil_translate, expected) 
            
    def test_tamil_translate_failure(self):
        for test in self.failure_test_tamil_translate:
            tamil_translate = app.bot_response_api(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(tamil_translate, expected)
            
    def test_parse_message_error_tamil_translate(self):
        for test in self.error_tamil_translate_test_params:
            tamil_translate = app.bot_response_api(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(tamil_translate, expected)
            
    def test_parse_message_error_funtranslate(self):
        for test in self.error_funtranslate_test_params:
            funtranslate = app.bot_response_api(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(funtranslate, expected)
            
    def test_text_to_binary_failure(self):
        for test_case in self.failure_test_text_to_binary:
            text_to_binary = bot_response_api(test_case[KEY_INPUT])
            expected = test_case[KEY_EXPECTED]
            self.assertEqual(text_to_binary, expected)  
    
  
    
            
if __name__ == '__main__':
    unittest.main()
