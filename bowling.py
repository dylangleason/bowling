import re


class BowlingScore:
    """BowlingScore calculates a running total bowling score after each
    frame is completed via the `complete_frame` method.

    """
    BONUS = 10
    MAX_PINS = 10
    STRIKE = 1
    TRIPLE = 5

    def __init__(self, max_frames: int = 10):
        self.strikes = []
        self.total_score = 0
        self.current_frame = 0
        self.spare = 0
        self.max_frames = max_frames

    def _accum_strikes(self, roll1: int, roll2: int, acc: int) -> int:
        new_sum = roll1 + roll2
        if not self.strikes:
            return acc
        new_roll1 = self.strikes.pop()
        frame_score = new_sum + new_roll1
        return self._accum_strikes(new_roll1, roll1, frame_score + acc)

    def _accum_score(self, score: int, roll1: int, roll2: int) -> None:
        if self.spare:
            self.total_score += score + roll1 + self.spare
            self.spare = 0
        else:
            self.total_score += self._accum_strikes(roll1, roll2, score)

    def _handle_strike(self) -> None:
        if self.spare:
            self._accum_score(self.BONUS, 0, 0)
        self.strikes.append(self.BONUS)

    def _handle_spare(self) -> None:
        if self.strikes:
            self._accum_score(self.BONUS, 0, 0)
        self.spare = self.BONUS

    def _handle_open_frame(self, frame: str) -> None:
        roll1, roll2 = frame.split(',')
        roll1, roll2 = int(roll1), int(roll2)
        score = roll1 + roll2

        if score > self.MAX_PINS:
            raise ValueError("Frame score must not exceed 10 pins")

        self._accum_score(score, roll1, roll2)

    def _handle_final_frame(self, frame: str) -> None:
        r1, r2, r3 = frame.split(',')
        if r1 == 'x':
            self.total_score += self.BONUS + int(r2) + int(r3)
        else:
            self.total_score += self.BONUS + int(r3)

    def _handle_double(self, frame: str) -> None:
        if '/' in frame:
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

    def complete_frame(self, frame: str) -> None:
        """Given a frame string with a valid frame format, complete the frame
        by accumulating the score and advancing to the next frame.

        """
        frame = frame.lower()
        self._validate_frame(frame)

        num_rolls = len(frame)
        if num_rolls == self.STRIKE:
            self._handle_strike()
        elif num_rolls == self.TRIPLE:
            self._handle_final_frame(frame)
        else:
            self._handle_double(frame)

        self.current_frame += 1
        

def _print_invalid_frame(message: str):
    print(f"ERROR: {message}. Please try again.\n")


def _print_current_score(scoreboard: BowlingScore):
    print(
        f"Next Frame: {scoreboard.current_frame+1}",
        f"Total: {scoreboard.total_score}\n"
    )


def _print_final_score(scoreboard: BowlingScore):
    print(f"Your final score is: {scoreboard.total_score}")


def _read_frame(scoreboard: BowlingScore):
    return input(f"Enter result for Frame {scoreboard.current_frame+1}: ")


def main():
    scoreboard = BowlingScore()
    while scoreboard.current_frame < scoreboard.max_frames:
        frame = _read_frame(scoreboard)
        try:
            scoreboard.complete_frame(frame)
            _print_current_score(scoreboard)
        except ValueError as err:
            _print_invalid_frame(err)
            continue
    _print_final_score(scoreboard)


if __name__ == '__main__':
    main()
