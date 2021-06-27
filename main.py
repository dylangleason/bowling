from bowling import BowlingScore


def _print_invalid_frame(message: str):
    print(f"ERROR: {message}. Please try again.\n")


def _print_current_score(scoreboard: BowlingScore):
    next_frame = scoreboard.current_frame+1
    if next_frame > 10:
        return
    print(f"Next Frame: {scoreboard.current_frame+1}, Total: {scoreboard.total_score}\n")


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
