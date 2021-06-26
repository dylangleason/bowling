from unittest import TestCase

from bowling import BowlingScore


class TestBowling(TestCase):

    def setUp(self):
        self.scoreboard = BowlingScore()

    def test_complete_frame__open_frame__reports_score(self):
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

    def test_complete_frame__strike_frame__does_not_report_score(self):
        self.scoreboard.complete_frame('X')
        self.assertEqual(self.scoreboard.total_score, 0)

    def test_complete_frame__strike_followed_by_open_frame__reports_score(self):
        self.scoreboard.complete_frame('X')
        self.scoreboard.complete_frame('2,1')
        self.assertEqual(self.scoreboard.total_score, 16)

    def test_complete_frame__strikes_consecutively__reports_score(self):
        self.scoreboard.complete_frame('X')
        self.scoreboard.complete_frame('X')
        self.scoreboard.complete_frame('X')
        self.scoreboard.complete_frame('2,3')
        self.assertEqual(self.scoreboard.total_score, 72)
