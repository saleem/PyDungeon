import unittest
from sys import maxsize
from unittest.mock import MagicMock
from pydungeon import get_input, MESSAGE_ROW, GameState, monster_move, init_map, get_player_move


class TestPyDungeon(unittest.TestCase):
    def test_get_input_does_not_display_message_when_it_is_default_value_and_converts_input_to_lowercase(self):
        # Arrange
        mock_window = MagicMock()
        mock_window.getkey.return_value = "ABC"

        # Act
        input = get_input(mock_window, "")

        # Assert
        mock_window.addstr.assert_not_called()
        mock_window.refresh.assert_not_called()
        self.assertEqual(input, "abc", "Should convert input to lowercase")

    def test_get_input_displays_message_when_provided_and_converts_input_to_lowercase(self):
        # Arrange
        mX = 20
        mY = 10
        given_message = "message"
        displayed_message = "message             "  # length == mX
        mock_window = MagicMock()
        mock_window.getmaxyx.return_value = (mY, mX)
        mock_window.getkey.return_value = "ABC"

        # Act
        input = get_input(mock_window, given_message)

        # Assert
        mock_window.addstr.assert_called_with(MESSAGE_ROW, 0, displayed_message)
        mock_window.refresh.assert_called_once()
        self.assertEqual(input, "abc", "Should convert input to lowercase")

    def test_monster_move_when_there_is_no_active_monster(self):
        # Arrange
        game_state = GameState()
        game_state.dungeon_map = init_map()
        game_state.player_map = init_map()
        mock_window = MagicMock()

        # Precondition
        self.assertEqual(game_state.player_map[0][0], ' ', "Player map should contain ' ' at (0,0) before monster move")

        # Act
        monster_move(mock_window, game_state)

        # Assert
        self.assertEqual(game_state.player_map[0][0], '', "Player map should contain '' at (0,0) after monster move")

    def test_monster_move_when_there_is_an_active_monster(self):
        # Arrange
        game_state = GameState()
        game_state.dungeon_map = init_map()
        game_state.player_map = init_map()
        game_state.active_monster = "X"
        mock_window = MagicMock()

        # Precondition
        self.assertEqual(game_state.player_map[0][0], ' ', "Player map should contain ' ' at (0,0) before monster move")

        # Act
        monster_move(mock_window, game_state)

        # Assert
        self.assertEqual(game_state.player_map[0][0], 'X', "Player map should contain 'X' at (0,0) after monster move")

    def test_get_player_move(self):
        # Arrange
        mX = 20
        mY = 10
        game_state = GameState()
        game_state.shift_mode = maxsize  # this should be overridden if test passes
        mock_window = MagicMock()
        mock_window.getkey.side_effect = ["A", "B", "Q"]   # only "Q" is a valid move
        mock_window.getmaxyx.return_value = (mY, mX)

        # Act
        input = get_player_move(mock_window, game_state)

        self.assertEqual(input, "q", "Should ignore invalid inputs and return lowercase valid input")
        self.assertEqual(game_state.shift_mode, 0, "Shift mode should be set to 0")
