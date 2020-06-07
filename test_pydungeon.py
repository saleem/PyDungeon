import unittest
from unittest.mock import MagicMock, patch
from pydungeon import get_input, MESSAGE_ROW

class TestPyDungeon(unittest.TestCase):
    def test_get_input_does_not_display_message_when_it_is_default_value_and_converts_input_to_lowercase(self):
        #Arrange
        mockWindow = MagicMock()
        mockWindow.getkey.return_value = "ABC"

        #Act
        input = get_input(mockWindow, "")

        #Assert
        mockWindow.addstr.assert_not_called()
        mockWindow.refresh.assert_not_called()
        self.assertEqual(input, "abc", "Should convert input to lowercase")


    def test_get_input_displays_message_when_provided_and_converts_input_to_lowercase(self):
        # Arrange
        mX = 20
        mY = 10
        givenMessage   = "message"
        displayedMessage = "message             " #length == mX
        mockWindow = MagicMock()
        mockWindow.getmaxyx.return_value = (mY, mX)
        mockWindow.getkey.return_value = "ABC"

        #Act
        input = get_input(mockWindow, "message")

        #Assert
        mockWindow.addstr.assert_called_with(MESSAGE_ROW, 0, displayedMessage)
        mockWindow.refresh.assert_called_once()
        self.assertEqual(input, "abc", "Should convert input to lowercase")
