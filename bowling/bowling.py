import re
from typing import List


class BowlingScore:
    """BowlingScore calculates a running total bowling score after each
    frame is completed via the `complete_frame` method.

    """
    BONUS = 10
    MAX_PINS = 10
    STRIKE = 'x'
    SPARE = '/'
    FINAL_FRAME = 5

    def __init__(self, max_frames: int = 10):
        self.strikes: List[int] = []
        self.total_score: int = 0
        self.current_frame: int = 0
        self.is_spare: bool = False
        self.max_frames: int = max_frames

    @property
    def _is_final_frame(self) -> bool:
        return self.current_frame == self.max_frames-1

    def complete_frame(self, frame: str) -> None:
        """Given a `frame` string with a valid frame format, complete the
        frame by accumulating the score and advancing to the next
        frame.

        Valid frame formats are:

           X     - Strike ("x" is also accepted as input)
           n,/   - Spare
           n,m   - Open Frame, where n and m are numbers

        For the final frame, valid frame formats are:

           n,m   - Open frame, where n and m are numbers
           X,n,m - Strike plus two bonus rolls
           n,/,m - Spare plus one bonus rolls
           X,X,n - Two strikes plus one bonus roll
           X,X,X - Three strikes
           X,n,/ - Strike plus two bonus rolls resulting in spare

        """
        frame = frame.lower()
        self._validate_frame(frame)

        points = self._handle_frame(frame)
        if len(points) > 1:
            r1 = points[0]
            r2 = points[1]
            self._accum_score(r1+r2, r1, r2)

        if self._is_final_frame and self.strikes:
            roll = points[0] if points else 0
            self._accum_score(roll, roll, 0)

        self.current_frame += 1

    def _accum_strikes(self, r1: int, r2: int, acc: int) -> int:
        new_sum = r1 + r2
        if not self.strikes:
            return acc
        new_r1 = self.strikes.pop()
        frame_score = new_sum + new_r1
        return self._accum_strikes(new_r1, r1, frame_score + acc)

    def _accum_score(self, score: int, r1: int, r2: int) -> None:
        if self.is_spare:
            self._accum_spare(score+r1)
        else:
            self.total_score += self._accum_strikes(r1, r2, score)

    def _accum_spare(self, roll: int) -> None:
        self.total_score += roll + self.BONUS
        self.is_spare = False

    def _handle_frame(self, frame: str) -> List[int]:
        points: List[int] = []

        for roll in frame.split(","):
            if roll == self.STRIKE:
                self._handle_strike()
            elif roll == self.SPARE:
                points = []
                self._handle_spare()
            else:
                r = int(roll)
                if self.is_spare:
                    self._accum_spare(r)
                points.append(r)

        return points

    def _handle_strike(self) -> None:
        if self.is_spare:
            self._accum_score(self.BONUS, 0, 0)
        self.strikes.append(self.BONUS)

    def _handle_spare(self) -> None:
        if self.strikes:
            self._accum_score(self.BONUS, 0, 0)
        self.is_spare = True

    def _validate_frame(self, frame: str) -> None:
        if not re.match(r'^(((x|\d),?)+\/?)(,\d)?$', frame):
            raise ValueError("Invalid frame format")
        if not self._is_final_frame and len(frame) >= self.FINAL_FRAME:
            raise ValueError("Three rolls are only allowed in the final Frame")
