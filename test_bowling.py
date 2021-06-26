from unittest import TestCase

from bowling import BowlingScore


class TestBowling(TestCase):

    def setUp(self):
        self.scoreboard = BowlingScore()

    def test_complete_frame__open_frame__updates_score(self):
        self.scoreboard.complete_frame('5,5')
        self.assertEqual(self.scoreboard.total_score, 10)

    def test_complete_frame__open_frames_accumulates_score(self):
        self.scoreboard.complete_frame('5,5')
        self.scoreboard.complete_frame('2,3')
        self.assertEqual(self.scoreboard.total_score, 15)

    def test_complete_frame__any_frame__increments_frame(self):
        self.scoreboard.complete_frame('X')
        self.scoreboard.complete_frame('2,4')
        self.assertEqual(self.scoreboard.current_frame, 2)

    def test_complete_frame__strike__does_not_update_score(self):
        self.scoreboard.complete_frame('X')
        self.assertEqual(self.scoreboard.total_score, 0)

    def test_complete_frame__strike_followed_by_open_frame__updates_score(self):
        self.scoreboard.complete_frame('X')
        self.scoreboard.complete_frame('2,1')
        self.assertEqual(self.scoreboard.total_score, 16)

    def test_complete_frame__strikes_consecutively__updates_score(self):
        self.scoreboard.complete_frame('X')
        self.scoreboard.complete_frame('X')
        self.scoreboard.complete_frame('X')
        self.scoreboard.complete_frame('2,3')
        self.assertEqual(self.scoreboard.total_score, 72)

    def test_complete_frame__spare__does_not_update_score(self):
        self.scoreboard.complete_frame('3,/')
        self.assertEqual(self.scoreboard.total_score, 0)

    def test_complete_frame__spare_followed_by_open_frame__updates_score(self):
        self.scoreboard.complete_frame('3,/')
        self.scoreboard.complete_frame('1,2')
        self.assertEqual(self.scoreboard.total_score, 14)

    def test_complete_frame__spare_followed_by_strike__updates_score(self):
        self.scoreboard.complete_frame('5,/')
        self.scoreboard.complete_frame('X')
        self.assertEqual(self.scoreboard.total_score, 20)

    def test_complete_frame__strike_followed_by_spare__updates_score(self):
        self.scoreboard.complete_frame('X')
        self.scoreboard.complete_frame('7,/')
        self.scoreboard.complete_frame('7,2')
        self.assertEqual(self.scoreboard.total_score, 46)

    def test_complete_frame__raises_error_for_invalid_frame(self):
        self.assertRaises(ValueError, self.scoreboard.complete_frame, 'foo')

    def test_complete_frame__final_frame__raises_error_when_not_last_frame(self):
        self.assertRaises(ValueError, self.scoreboard.complete_frame, 'X,1,2')

    def test_complete_frame__final_frame__with_strike__updates_score(self):
        self.scoreboard.current_frame = 10
        self.scoreboard.complete_frame('X,5,5')
        self.assertEqual(self.scoreboard.total_score, 20)

    def test_complete_frame__final_frame__with_spare__updates_score(self):
        self.scoreboard.current_frame = 10
        self.scoreboard.complete_frame('2,/,3')
        self.assertEqual(self.scoreboard.total_score, 13)

    def test_complete_frame__final_frame__with_open_frame__updates_score(self):
        self.scoreboard.current_frame = 10
        self.scoreboard.complete_frame('2,5')
        self.assertEqual(self.scoreboard.total_score, 7)
