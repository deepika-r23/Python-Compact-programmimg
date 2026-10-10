import time


class Player:
    """Stores information about one player."""

    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.number_of_moves = 0
        self.result = "Unfinished"

    def record_move(self):
        self.number_of_moves += 1

    def set_result(self, result):
        self.result = result


class Checker:
    """Represents one checker piece."""

    def __init__(self, color, row, column):
        self.color = color
        self.row = row
        self.column = column
        self.is_king = False

    def make_king(self):
        self.is_king = True

    def symbol(self):
        if self.color == "red":
            return "R" if self.is_king else "r"
        return "B" if self.is_king else "b"

    def allowed_directions(self):
        # Red moves toward row 0; black moves toward row 7.
        if self.is_king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        if self.color == "red":
            return [(-1, -1), (-1, 1)]
        return [(1, -1), (1, 1)]


class Board:
    """Stores and updates the 8x8 board."""

    SIZE = 8

    def __init__(self):
        self.squares = [[None for _ in range(self.SIZE)]
                        for _ in range(self.SIZE)]
        self.initialize_board()

    def initialize_board(self):
        # Black starts at the top and red starts at the bottom.
        for row in range(3):
            for column in range(self.SIZE):
                if (row + column) % 2 == 1:
                    self.squares[row][column] = Checker("black", row, column)

        for row in range(5, 8):
            for column in range(self.SIZE):
                if (row + column) % 2 == 1:
                    self.squares[row][column] = Checker("red", row, column)

    @staticmethod
    def in_bounds(row, column):
        return 0 <= row < 8 and 0 <= column < 8

    def display(self):
        print("\n    0 1 2 3 4 5 6 7")
        print("   -----------------")
        for row in range(self.SIZE):
            cells = []
            for column in range(self.SIZE):
                checker = self.squares[row][column]
                cells.append(checker.symbol() if checker else ".")
            print(f"{row} | " + " ".join(cells))
        print("   -----------------")
        print("r = red, b = black, R/B = king, . = empty\n")

    def count_checkers(self, color):
        return sum(
            1
            for row in self.squares
            for checker in row
            if checker is not None and checker.color == color
        )

    def has_piece(self, color):
        return self.count_checkers(color) > 0

    def has_legal_move(self, color):
        for row in range(self.SIZE):
            for column in range(self.SIZE):
                checker = self.squares[row][column]
                if checker is None or checker.color != color:
                    continue

                for dr, dc in checker.allowed_directions():
                    next_row, next_column = row + dr, column + dc
                    if not self.in_bounds(next_row, next_column):
                        continue

                    if self.squares[next_row][next_column] is None:
                        return True

                    # A capture is possible if an opponent is next to the
                    # checker and the square beyond it is empty.
                    middle = self.squares[next_row][next_column]
                    land_row, land_column = row + 2 * dr, column + 2 * dc
                    if (
                        middle is not None
                        and middle.color != color
                        and self.in_bounds(land_row, land_column)
                        and self.squares[land_row][land_column] is None
                    ):
                        return True
        return False

    def move_checker(self, start_row, start_col, end_row, end_col, color):
        """Move a checker if the move is legal. Return (success, message, captured)."""
        coordinates = (start_row, start_col, end_row, end_col)
        if not all(isinstance(value, int) for value in coordinates):
            return False, "Rows and columns must be whole numbers.", False

        if not self.in_bounds(start_row, start_col) or not self.in_bounds(end_row, end_col):
            return False, "Coordinates must be between 0 and 7.", False

        checker = self.squares[start_row][start_col]
        if checker is None:
            return False, "There is no checker at the starting position.", False
        if checker.color != color:
            return False, "That checker belongs to the other player.", False
        if self.squares[end_row][end_col] is not None:
            return False, "The destination square is occupied.", False

        dr = end_row - start_row
        dc = end_col - start_col
        if abs(dr) != abs(dc):
            return False, "Checkers move diagonally.", False

        directions = checker.allowed_directions()
        if (dr, dc) in directions and abs(dr) == 1:
            self.squares[end_row][end_col] = checker
            self.squares[start_row][start_col] = None
            checker.row, checker.column = end_row, end_col
            self.promote_if_needed(checker)
            return True, "Move completed.", False

        if abs(dr) == 2 and (dr // 2, dc // 2) in directions:
            middle_row = (start_row + end_row) // 2
            middle_col = (start_col + end_col) // 2
            middle_checker = self.squares[middle_row][middle_col]

            if middle_checker is None or middle_checker.color == color:
                return False, "A capture must jump over an opponent's checker.", False

            self.squares[end_row][end_col] = checker
            self.squares[start_row][start_col] = None
            self.squares[middle_row][middle_col] = None
            checker.row, checker.column = end_row, end_col
            self.promote_if_needed(checker)
            return True, "Capture completed.", True

        return False, "That move is not legal for this checker.", False

    @staticmethod
    def promote_if_needed(checker):
        if checker.color == "red" and checker.row == 0:
            checker.make_king()
        elif checker.color == "black" and checker.row == 7:
            checker.make_king()


class Game:
    """Coordinates players, turns, timing, and the game summary."""

    def __init__(self, player1_name, player2_name):
        self.players = [
            Player(player1_name, "red"),
            Player(player2_name, "black"),
        ]
        self.board = Board()
        self.current_player_index = 0
        self.total_moves = 0
        self.start_time = None
        self.end_time = None
        self.finish_reason = "Game finished by a player."

    @property
    def current_player(self):
        return self.players[self.current_player_index]

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def play_turn(self):
        player = self.current_player
        print(f"\n{player.name} ({player.color}) — your turn")
        print(f"Your moves: {player.number_of_moves}")
        print("1. Make a move")
        print("2. Finish the game")
        choice = input("Choose 1 or 2: ").strip()

        if choice == "2":
            self.finish_reason = f"{player.name} chose to finish the game."
            return False
        if choice != "1":
            print("Please enter 1 or 2. It is still your turn.")
            return True

        try:
            print("Enter coordinates from 0 to 7.")
            start_row = int(input("Starting row: "))
            start_col = int(input("Starting column: "))
            end_row = int(input("Destination row: "))
            end_col = int(input("Destination column: "))
        except ValueError:
            print("Invalid input. Please enter whole numbers.")
            return True

        success, message, captured = self.board.move_checker(
            start_row, start_col, end_row, end_col, player.color
        )
        print(message)

        if not success:
            return True

        player.record_move()
        self.total_moves += 1
        print(f"Move {self.total_moves} completed by {player.name}.")
        if captured:
            print("An opponent's checker was captured.")

        self.board.display()

        opponent = self.players[1 - self.current_player_index]
        if self.board.count_checkers(opponent.color) == 0:
            player.set_result("Winner")
            opponent.set_result("Loser")
            self.finish_reason = f"{player.name} won by capturing all opponent checkers."
            return False

        if not self.board.has_legal_move(opponent.color):
            player.set_result("Winner")
            opponent.set_result("Loser")
            self.finish_reason = f"{player.name} won because {opponent.name} has no legal moves."
            return False

        self.switch_player()
        return True

    def show_summary(self):
        if self.end_time is None:
            self.end_time = time.time()
        duration = int(self.end_time - self.start_time) if self.start_time else 0
        minutes, seconds = divmod(duration, 60)

        print("\n========== GAME SUMMARY ==========")
        for player in self.players:
            print(f"Player: {player.name}")
            print(f"Color: {player.color}")
            print(f"Valid moves: {player.number_of_moves}")
            print(f"Result: {player.result}")
            print()

        print(f"Total valid moves: {self.total_moves}")
        print(f"Duration: {minutes:02d}:{seconds:02d}")
        print(f"Reason: {self.finish_reason}")
        print("==================================")

    def start(self):
        self.start_time = time.time()
        print("\nWelcome to Checkers!")
        print("Red moves first. Use row and column numbers from 0 to 7.")
        self.board.display()

        game_is_running = True
        while game_is_running:
            game_is_running = self.play_turn()

        self.end_time = time.time()

        # If a winner has not been determined, record the game as unfinished.
        if all(player.result == "Unfinished" for player in self.players):
            for player in self.players:
                player.set_result("Game ended without a winner")

        self.show_summary()


def main():
    print("=== Two-player Checkers ===")
    player1_name = input("Enter the name of the red player: ").strip() or "Player 1"
    player2_name = input("Enter the name of the black player: ").strip() or "Player 2"

    game = Game(player1_name, player2_name)
    game.start()


if __name__ == "__main__":
    main()
