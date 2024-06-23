import tkinter as tk
from PIL import Image, ImageTk
from chess_gameplay import GamePlay

class ChessBoard(tk.Frame):
    def __init__(self, master, game):
        super().__init__(master)
        self.master = master
        self.game = game
        self.grid()
        self.square_size = 60
        self.create_board()
        self.highlighted = []
        self.selected_square = None
        self.drag_data = {"piece": None, "start_square": None, "overlay": None}

    def create_board(self):
        self.squares = {}
        self.images = self.load_images()
        colors = ['#DDB88C', '#A66D4F']
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                square = tk.Frame(self, width=self.square_size, height=self.square_size, bg=color)
                square.grid(row=row, column=col)
                self.squares[(row, col)] = square
                piece = self.game.board.get_piece(row, col)
                if piece:
                    label = tk.Label(square, image=self.images[piece], bg=color)
                    label.bind("<ButtonPress-1>", self.on_drag_start)
                    label.bind("<ButtonRelease-1>", self.on_drag_end)
                    label.bind("<B1-Motion>", self.on_drag_motion)
                    label.place(x=0, y=0, width=self.square_size, height=self.square_size)

    def load_images(self):
        pieces = ['br', 'bn', 'bb', 'bq', 'bk', 'bp', 'wr', 'wn', 'wb', 'wq', 'wk', 'wp']
        images = {}
        for piece in pieces:
            try:
                img = Image.open(f"images/{piece}.png")
                img = img.resize((self.square_size, self.square_size), Image.LANCZOS)
                images[piece] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading image for piece {piece}: {e}")
                images[piece] = None
        return images

    def highlight_square(self, row, col, color):
        for r, c in self.highlighted:
            self.squares[(r, c)].config(bg=self.original_color(r, c))
        if color == "default":
            self.highlighted = []
        else:
            self.squares[(row, col)].config(bg=color)
            self.highlighted = [(row, col)]

    def original_color(self, row, col):
        return '#DDB88C' if (row + col) % 2 == 0 else '#A66D4F'

    def update_board(self):
        for row in range(8):
            for col in range(8):
                square = self.squares[(row, col)]
                theSquare = chr(97 + col) + str(8 - row)
                for widget in square.winfo_children():
                    widget.destroy()
                piece = self.game.board.get_piece(row, col)
                if piece:
                    label = tk.Label(square, image=self.images[piece], bg=square.cget('bg'))
                    label.bind("<ButtonPress-1>", self.on_drag_start)
                    label.bind("<ButtonRelease-1>", self.on_drag_end)
                    label.bind("<B1-Motion>", self.on_drag_motion)
                    label.place(x=0, y=0, width=self.square_size, height=self.square_size)

    def on_drag_start(self, event):
        widget = event.widget
        self.drag_data["piece"] = widget
        self.drag_data["start_square"] = (widget.master.grid_info()["row"], widget.master.grid_info()["column"])

        # Create an overlay label for dragging
        self.drag_data["overlay"] = tk.Label(self.master, image=widget.cget("image"), bg=None)
        self.drag_data["overlay"].place(x=widget.winfo_rootx() - self.master.winfo_rootx(),
                                        y=widget.winfo_rooty() - self.master.winfo_rooty(), anchor="nw")
        widget.place_forget()

    def on_drag_end(self, event):
        overlay = self.drag_data["overlay"]
        start_row, start_col = self.drag_data["start_square"]

        # Get the drop target row and column
        x = self.master.winfo_pointerx() - self.master.winfo_rootx()
        y = self.master.winfo_pointery() - self.master.winfo_rooty()
        target_col = x // self.square_size
        target_row = y // self.square_size

        # Check if the drop is within the board boundaries
        if 0 <= target_row < 8 and 0 <= target_col < 8:
            from_square = chr(97 + start_col) + str(8 - start_row)
            to_square = chr(97 + target_col) + str(8 - target_row)
            print(from_square, to_square)

            if self.game.is_valid_move(from_square, to_square):
                self.game.move_piece(from_square, to_square)
                self.update_board()
            else:
                self.reset_piece()
        else:
            self.reset_piece()

        if overlay:
            overlay.destroy()

        self.drag_data["piece"] = None
        self.drag_data["start_square"] = None
        self.drag_data["overlay"] = None

    def reset_piece(self):
        piece = self.drag_data["piece"]
        row, col = self.drag_data["start_square"]
        piece.place(in_=self.squares[(row, col)], x=0, y=0, width=self.square_size, height=self.square_size)

    def on_drag_motion(self, event):
        overlay = self.drag_data.get("overlay")
        if overlay:
            x = self.master.winfo_pointerx() - self.master.winfo_rootx() - self.square_size // 2
            y = self.master.winfo_pointery() - self.master.winfo_rooty() - self.square_size // 2
            overlay.place(x=x, y=y)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Chess GUI")
    game = GamePlay()
    ChessBoard(root, game)
    root.mainloop()
