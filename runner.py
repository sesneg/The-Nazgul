"""
runner.py  –  Tkinter GUI for Minimax Tic-Tac-Toe
Human plays against the AI.  Human is O, AI is X.
"""
import tkinter as tk
from tkinter import messagebox
from tictactoe import (initial_state, player, actions, result,
                       winner, terminal, utility, minimax, X, O, EMPTY)

BG       = "#1a1a2e"
CELL_BG  = "#16213e"
X_COLOR  = "#e94560"
O_COLOR  = "#0f3460"
TEXT_COL = "#ffffff"
BTN_COL  = "#533483"

CELL_SIZE = 160
FONT_MARK = ("Helvetica", 72, "bold")
FONT_MSG  = ("Helvetica", 22, "bold")
FONT_BTN  = ("Helvetica", 14, "bold")

class TicTacToeApp:
    def __init__(self, root):
        self.root  = root
        self.root.title("Tic-Tac-Toe  |  Minimax AI")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self.board      = initial_state()
        self.human      = O     # human is O
        self.ai         = X     # AI is X
        self.game_over  = False

        self._build_ui()
        self._refresh()

        # AI goes first if it's X's turn at the start
        if player(self.board) == self.ai:
            self.root.after(400, self._ai_move)

    # UI construction 
    def _build_ui(self):
        self.msg_var = tk.StringVar(value="Your turn  (O)")
        msg_lbl = tk.Label(self.root, textvariable=self.msg_var,
                           font=FONT_MSG, bg=BG, fg=TEXT_COL, pady=12)
        msg_lbl.pack()

        canvas_frame = tk.Frame(self.root, bg=BG)
        canvas_frame.pack()

        total = CELL_SIZE * 3
        self.canvas = tk.Canvas(canvas_frame, width=total, height=total,
                                bg=CELL_BG, highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_click)

        self.btn = tk.Button(self.root, text="Play Again",
                             font=FONT_BTN, bg=BTN_COL, fg=TEXT_COL,
                             relief="flat", padx=20, pady=8,
                             command=self._reset)
        self.btn.pack(pady=14)

    # draw board
    def _refresh(self):
        self.canvas.delete("all")
        cs = CELL_SIZE

        # grid lines
        for i in range(1, 3):
            self.canvas.create_line(i*cs, 0, i*cs, 3*cs, fill="#ffffff", width=3)
            self.canvas.create_line(0, i*cs, 3*cs, i*cs, fill="#ffffff", width=3)

        # marks
        for r in range(3):
            for c in range(3):
                mark = self.board[r][c]
                if mark:
                    cx = c * cs + cs // 2
                    cy = r * cs + cs // 2
                    color = X_COLOR if mark == X else O_COLOR
                    self.canvas.create_text(cx, cy, text=mark,
                                            font=FONT_MARK, fill=color)

    # click handler
    def _on_click(self, event):
        if self.game_over or player(self.board) != self.human:
            return
        cs   = CELL_SIZE
        col  = event.x // cs
        row  = event.y // cs
        move = (row, col)

        if move not in actions(self.board):
            return

        self.board = result(self.board, move)
        self._refresh()
        self._check_end()

        if not self.game_over:
            self.msg_var.set("AI is thinking…")
            self.root.after(300, self._ai_move)

    # AI move
    def _ai_move(self):
        if self.game_over:
            return
        move = minimax(self.board)
        if move:
            self.board = result(self.board, move)
        self._refresh()
        self._check_end()
        if not self.game_over:
            self.msg_var.set("Your turn  (O)")

    # check terminal
    def _check_end(self):
        if terminal(self.board):
            self.game_over = True
            w = winner(self.board)
            if w:
                self.msg_var.set(f"Game Over:  {w} wins!")
            else:
                self.msg_var.set("Game Over:  It's a tie!")

    def _reset(self):
        self.board     = initial_state()
        self.game_over = False
        self.msg_var.set("Your turn  (O)")
        self._refresh()
        if player(self.board) == self.ai:
            self.root.after(400, self._ai_move)

if __name__ == "__main__":
    root = tk.Tk()
    app  = TicTacToeApp(root)
    root.mainloop()
