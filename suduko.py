import tkinter as tk
from tkinter import messagebox, ttk
import random

class SudokuSolver:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Sudoku Solver")
        self.cells = [[None for _ in range(9)] for _ in range(9)]
        self.difficulty = tk.StringVar(value="Easy")
        self.create_grid()
        self.create_buttons()
    
    def create_grid(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.reset_grid()
    
    def create_buttons(self):
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        
        solve_button = tk.Button(button_frame, text="Solve", command=self.solve_sudoku, font=("Arial", 16), width=10, bg="lightblue")
        solve_button.grid(row=0, column=0, padx=5, pady=5)
        
        reset_button = tk.Button(button_frame, text="Reset", command=self.reset_grid, font=("Arial", 16), width=10, bg="lightcoral")
        reset_button.grid(row=0, column=1, padx=5, pady=5)
        
        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_grid, font=("Arial", 16), width=10, bg="lightyellow")
        clear_button.grid(row=0, column=2, padx=5, pady=5)
        
        difficulty_label = tk.Label(button_frame, text="Difficulty:", font=("Arial", 14))
        difficulty_label.grid(row=1, column=0, padx=5, pady=5)
        
        difficulty_menu = ttk.Combobox(button_frame, textvariable=self.difficulty, values=["Easy", "Medium", "Hard"], font=("Arial", 14), state="readonly")
        difficulty_menu.grid(row=1, column=1, padx=5, pady=5)
        difficulty_menu.current(0)
    
    def get_grid(self):
        grid = []
        for i in range(9):
            row = []
            for j in range(9):
                value = self.cells[i][j].get()
                row.append(int(value) if value.isdigit() else 0)
            grid.append(row)
        return grid
    
    def set_grid(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] != 0:
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, str(grid[i][j]))
    
    def is_valid(self, grid, row, col, num):
        for i in range(9):
            if grid[row][i] == num or grid[i][col] == num:
                return False
        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if grid[start_row + i][start_col + j] == num:
                    return False
        return True
    
    def solve(self, grid):
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(grid, i, j, num):
                            grid[i][j] = num
                            if self.solve(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True
    
    def solve_sudoku(self):
        grid = self.get_grid()
        if self.solve(grid):
            self.set_grid(grid)
        else:
            messagebox.showerror("Error", "No solution exists!")
    
    def reset_grid(self):
        colors = ["#FFC0CB", "#ADD8E6", "#90EE90", "#FFD700", "#FFA07A", "#DDA0DD", "#20B2AA", "#F0E68C", "#E6E6FA"]
        difficulty_levels = {"Easy": 40, "Medium": 30, "Hard": 20}
        num_clues = difficulty_levels[self.difficulty.get()]
        
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        base_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solve(base_grid)
        
        masked_grid = [row[:] for row in base_grid]
        for _ in range(81 - num_clues):
            x, y = random.randint(0, 8), random.randint(0, 8)
            while masked_grid[x][y] == 0:
                x, y = random.randint(0, 8), random.randint(0, 8)
            masked_grid[x][y] = 0
        
        for i in range(9):
            for j in range(9):
                color = random.choice(colors)
                entry = tk.Entry(self.frame, width=3, font=("Arial", 20), justify="center", borderwidth=2, relief="solid", bg=color)
                entry.grid(row=i, column=j, padx=2, pady=2)
                self.cells[i][j] = entry
                if masked_grid[i][j] != 0:
                    entry.insert(0, str(masked_grid[i][j]))
                    entry.config(state="disabled")
    
    def clear_grid(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j]["state"] == "normal":
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].config(bg="white")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuSolver(root)
    root.mainloop()
