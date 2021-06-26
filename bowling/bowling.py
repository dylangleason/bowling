import re
from typing import List


class BowlingScore:
    """BowlingScore calculates a running total bowling score after each
    frame is completed via the `complete_frame` method.

    """
    BONUS = 10
    MAX_PINS = 10
    SINGLE = 1
    TRIPLE = 5
    STRIKE = 'x'
    SPARE = '/'

    def __init__(self, max_frames: int = 10):
        self.strikes: List[int] = []
        self.total_score: int = 0
        self.current_frame: int = 0
        self.spare: int = 0
        self.max_frames: int = max_frames

    def complete_frame(self, frame: str) -> None:
        """Given a frame string with a valid frame format, complete the frame
        by accumulating the score and advancing to the next frame.

        """
        frame = frame.lower()
        self._validate_frame(frame)

        num_rolls = len(frame)
        if num_rolls == self.SINGLE:
            self._handle_strike()
        elif num_rolls == self.TRIPLE:
            self._handle_final_frame(frame)
        else:
            self._handle_double(frame)

        self.current_frame += 1

    def _accum_strikes(self, r1: int, r2: int, acc: int) -> int:
        new_sum = r1 + r2
        if not self.strikes:
            return acc
        new_r1 = self.strikes.pop()
        frame_score = new_sum + new_r1
        return self._accum_strikes(new_r1, r1, frame_score + acc)

    def _accum_score(self, score: int, r1: int, r2: int) -> None:
        if self.spare:
            self.total_score += score + r1 + self.spare
            self.spare = 0
        else:
            self.total_score += self._accum_strikes(r1, r2, score)

    def _handle_strike(self) -> None:
        if self.spare:
            self._accum_score(self.BONUS, 0, 0)
        self.strikes.append(self.BONUS)

    def _handle_spare(self) -> None:
        if self.strikes:
            self._accum_score(self.BONUS, 0, 0)
        self.spare = self.BONUS

    def _handle_open_frame(self, frame: str) -> None:
        r1, r2 = frame.split(',')
        r1, r2 = int(r1), int(r2)
        score = r1 + r2

        if score > self.MAX_PINS:
            raise ValueError("Frame score must not exceed 10 pins")

        self._accum_score(score, r1, r2)

    def _handle_final_frame(self, frame: str) -> None:
        r1, r2, r3 = frame.split(',')
        if r1 == self.STRIKE:
            self._accum_score(self.BONUS + int(r2) + int(r3), self.BONUS, int(r2))
        else:
            self._accum_score(self.BONUS + int(r3), int(r1), self.BONUS)

    def _handle_double(self, frame: str) -> None:
        if self.SPARE in frame:
            self._handle_spare()
        else:
            self._handle_open_frame(frame)

    def _validate_frame(self, frame: str) -> None:
        frame_pattern = re.match(r'^x|(\d,(\d|\/))$', frame)
        final_frame_pattern = re.match(r'^((x,\d)|(\d,\/)),\d$', frame)
        if not(frame_pattern or final_frame_pattern):
            raise ValueError("Invalid frame format")
        if self.current_frame < self.max_frames and final_frame_pattern:
            raise ValueError("Three rolls are only allowed in the final Frame")
