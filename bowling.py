import re


class BowlingScore:
    """BowlingScore calculates a running total bowling score after each
    frame is completed via the `complete_frame` method.

    """
    MAX_PINS = 10
    BONUS = 10

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

    def complete_frame(self, frame: str) -> None:
        """Given a frame string matching the format "X", "n,/" or "n,m",
        complete the frame by accumulating the score and advancing to
        the next frame.
        """
        frame = frame.lower()
        if not _is_valid_frame(frame):
            raise ValueError("Frame must match format: 'X', 'n,/' or 'n,m'")

        if frame == 'x':
            self._handle_strike()
        elif '/' in frame:
            self._handle_spare()
        else:
            self._handle_open_frame(frame)

        self.current_frame += 1


def _is_valid_frame(frame: str) -> bool:
    return frame == 'x' or re.match(r'^\d,(\d|\/)$', frame)
        

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
