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

    def test_complete_frame__strike_followed_by_open_frame__updates_score(self):
        # x    -> 10
        # x'   -> 10, x  -> 23
        # 3,0  -> 3,  x' -> 13
        #
        # Total: 39
        self.scoreboard.complete_frame('X')
        self.scoreboard.complete_frame('X')
        self.scoreboard.complete_frame('3,0')
        self.assertEqual(self.scoreboard.total_score, 39)

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
        self.scoreboard.current_frame = 9
        self.scoreboard.complete_frame('X,5,5')
        self.assertEqual(self.scoreboard.total_score, 30)

    def test_complete_frame__final_frame__with_spare__updates_score(self):
        self.scoreboard.current_frame = 9
        self.scoreboard.complete_frame('2,/,3')
        self.assertEqual(self.scoreboard.total_score, 13)

    def test_complete_frame__final_frame__with_open_frame__updates_score(self):
        self.scoreboard.current_frame = 9
        self.scoreboard.complete_frame('2,5')
        self.assertEqual(self.scoreboard.total_score, 7)

    def test_complete_frame__spare_followed_by_final_frame_with_spare__updates_score(
            self
    ):
        # 6,/ = 10
        # 7,/,3 = 13, 6,/' = 17
        # 10 + 17 + 3 = 30
        self.scoreboard.current_frame = 8
        self.scoreboard.complete_frame('6,/')
        self.scoreboard.current_frame = 9
        self.scoreboard.complete_frame('7,/,3')
        self.assertEqual(self.scoreboard.total_score, 30)

    def test_complete_frame__strike_followed_by_final_frame_with_spare__updates_score(
            self
    ):
        # X = 10  ->  7,/    = 20
        # 7,/,3   ->  10 + 3 = 13
        #
        # Total: 33
        self.scoreboard.current_frame = 8
        self.scoreboard.complete_frame('X')
        self.scoreboard.current_frame = 9
        self.scoreboard.complete_frame('7,/,3')
        #self.assertEqual(self.scoreboard.total_score, 40)
        self.assertEqual(self.scoreboard.total_score, 33)

    def test_complete_frame__spare_followed_by_final_frame_with_strike__updates_score(
            self
    ):
        # 6,/ = 10 -> 6,/,X = 20
        # X   = 10 -> X,5,2 = 17
        # 5,2 = 7  ->       =  7
        #
        # Total: 44
        self.scoreboard.current_frame = 8
        self.scoreboard.complete_frame('6,/')
        self.scoreboard.current_frame = 9
        self.scoreboard.complete_frame('X,5,2')
        self.assertEqual(self.scoreboard.total_score, 44)

    def test_complete_frame__strike_followed_by_final_frame_with_strike__updates_score(
            self
    ):
        # X     = 10 -> X,X,5 = 25
        # X,5,2 = 10 -> X,5,2 = 17
        # 5,2   = 7  ->          7
        #
        # Total: 49
        self.scoreboard.current_frame = 8
        self.scoreboard.complete_frame('X')
        self.scoreboard.current_frame = 9
        self.scoreboard.complete_frame('X,5,2')
        self.assertEqual(self.scoreboard.total_score, 49)

    def test_complete_frame__final_frame__with_two_strikes_and_point__updates_score(self):
        self.scoreboard.current_frame = 9
        self.scoreboard.complete_frame('X,X,3')
        self.assertEqual(self.scoreboard.total_score, 39)

    def test_complete_frame__final_frame__with_three_strikes__updates_score(self):
        self.scoreboard.current_frame = 9
        self.scoreboard.complete_frame('X,X,X')
        self.assertEqual(self.scoreboard.total_score, 60)

    def test_complete_frame__final_frame__with_strike_and_spare__updates_score(self):
        self.scoreboard.current_frame = 9
        self.scoreboard.complete_frame('X,5,/')
        self.assertEqual(self.scoreboard.total_score, 20)
