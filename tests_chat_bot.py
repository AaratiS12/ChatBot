'''
    This file tests all methods in app.py.
'''

import unittest
import app
#import KEY_IS_BOT, KEY_BOT_COMMAND, KEY_MESSAGE


KEY_INPUT = "input"
KEY_EXPECTED = "expected"
KEY_LENGTH = "length"
KEY_FIRST_WORD = "first_word"
KEY_SECOND_WORD = "second_word"

class ChatbotTestCase(unittest.TestCase):
    def setUp(self):
        self.success_test_params = [
            {
                KEY_INPUT: "!! help",
                KEY_EXPECTED: "Type either: \n1)!! translate/funtranslate {text}\n2)!! tamil-translate {text}\n3)!! random-fact\n4)!! text-to-binary {text}\n5)!! help\n6)!! about"
            },
            {
                KEY_INPUT: "!! about me",
                KEY_EXPECTED: "I am a bot, I will respond to messages that start with !!"
            },
            {
                KEY_INPUT: "!! tamil-translate coconut",
                KEY_EXPECTED: "தேங்காய்"
            },
            {
                KEY_INPUT: "! tamil-translate coconut",
                KEY_EXPECTED: "Command not found"
            },
           
            # TODO HW13 - add another
        ]
        
        self.failure_test_params = [
            {
                KEY_INPUT: "!! tamil-translate coconuts",
                KEY_EXPECTED: "my name is"
            },
             
        ]
        self.error_tamil_translate_test_params = [
            {
                KEY_INPUT: "!! tamil-translate",
                KEY_EXPECTED: "Error: text not given" 
            },
        ]
        self.error_funtranslate_test_params = [
            {
                KEY_INPUT: "!! funtranslate",
                KEY_EXPECTED: "Error: text not given" 
            },
            ]

    def test_parse_message_success(self):
        for test in self.success_test_params:
            response = app.bot_response_api(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
            
    def test_parse_message_failure(self):
        for test in self.failure_test_params:
            response = app.bot_response_api(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertNotEqual(response, expected)
            
    def test_parse_message_error_tamil_translate(self):
        for test in self.error_tamil_translate_test_params:
            response = app.bot_response_api(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
    def test_parse_message_error_funtranslate(self):
        for test in self.error_funtranslate_test_params:
            response = app.bot_response_api(test[KEY_INPUT])
            expected = test[KEY_EXPECTED]
            self.assertEqual(response, expected)
    
if __name__ == '__main__':
    unittest.main()
