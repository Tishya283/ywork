class Sudoku:
    def __init__(self, board):
        self.board = board

    def is_valid(self, row, col, num):
        # for row
        for x in range(9):
            if self.board[row][x] == num:
                return False

        # for column
        for x in range(9):
            if self.board[x][col] == num:
                return False

        # for 3x3 subgrid
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False

        return True

    def solve(self):
        empty_cell = self.find_empty()
        if not empty_cell:
            return True  # solved

        row, col = empty_cell
        for num in map(str, range(1, 10)):  
            if self.is_valid(row, col, num):
                self.board[row][col] = num
                if self.solve():
                    return True
                self.board[row][col] = "."  

        return False

    def find_empty(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == ".":
                    return (i, j)
        return None


def solve_sudoku(board):
    sudoku = Sudoku(board)
    sudoku.solve()
    return sudoku.board  


if __name__ == "__main__":
    board = [
        ["5","3",".",".","7",".",".",".","."],
        ["6",".",".","1","9","5",".",".","."],
        [".","9","8",".",".",".",".","6","."],
        ["8",".",".",".","6",".",".",".","3"],
        ["4",".",".","8",".","3",".",".","1"],
        ["7",".",".",".","2",".",".",".","6"],
        [".","6",".",".",".",".","2","8","."],
        [".",".",".","4","1","9",".",".","5"],
        [".",".",".",".","8",".",".","7","9"]
    ]

    print("Original Sudoku:")
    for row in board:
        print(row)

    solve_sudoku(board)

    print("\nSolved Sudoku:")
    for row in board:
        print(row)
