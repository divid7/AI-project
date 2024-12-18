import random
import math
import tkinter as tk
from tkinter import messagebox

# رجب المتص ومروان المحترم وجلجل ابو طيز كبيره احلي تحيه للرجاله المظبوطه


# invalid هنا الفانكشن بتشوف الرقم لو موجود ف نفس الصف او العمود يبقي
def is_valid(board, row, col, num):
    grid_size = len(board)
    for x in range(grid_size):
        if board[row][x] == num or board[x][col] == num:
            return False

    subgrid_size = int(math.sqrt(grid_size))
    start_row, start_col = row - row % subgrid_size, col - col % subgrid_size
    for i in range(subgrid_size):
        for j in range(subgrid_size):
            if board[start_row + i][start_col + j] == num:
                return False

    return True


# هنا بقي الفانكشن دي بتحل السودوكو خطوه خطوه علشان الي بيلعب يشوف براحه كده
def solve_sudoku_step_by_step(board, cells, button, delay=500):
    size = len(board)

    def backtrack_step(row, col):
        if row == size:
            return True

        next_row, next_col = (row, col + 1) if col + 1 < size else (row + 1, 0)

        if board[row][col] != 0:
            return backtrack_step(next_row, next_col)

        for num in range(1, size + 1):
            if is_valid(board, row, col, num):
                board[row][col] = num
                cells[row][col].delete(0, tk.END)
                cells[row][col].insert(0, str(num))
                cells[row][col].update()
                root.after(delay)

                if backtrack_step(next_row, next_col):
                    return True

                board[row][col] = 0
                cells[row][col].delete(0, tk.END)
                cells[row][col].update()
                root.after(delay)

        return False

    backtrack_step(0, 0)

    # إعادة تفعيل الزر ليكون قابلاً للنقر مرة أخرى
    button.config(state="normal")


# فانكشن هنا الي بتحل السودوكو بالباك تراك
def solve_sudoku_backtrack(board):
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                for num in range(1, size + 1):
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve_sudoku_backtrack(board):
                            return True
                        board[i][j] = 0
                return False
    return True


# الفانكشن هنا هي الي بتعمل السودوكو وبتحط الارقام العشوائيه فيه
def generate_sudoku(size, filled_numbers=41):
    board = [[0] * size for _ in range(size)]

    def fill_board(board):
        size = len(board)
        nums = list(range(1, size + 1))
        for i in range(size):
            for j in range(size):
                random.shuffle(nums)
                for num in nums:
                    if is_valid(board, i, j, num):
                        board[i][j] = num
                        if solve_sudoku_backtrack(board):
                            return True
                        board[i][j] = 0
                return False
        return True

    fill_board(board)

    total_cells = size * size
    cells_to_remove = total_cells - filled_numbers
    while cells_to_remove > 0:
        i, j = random.randint(0, size - 1), random.randint(0, size - 1)
        if board[i][j] != 0:
            board[i][j] = 0
            cells_to_remove -= 1

    return board


# الفانكشن دي الي بنعمل بيها ريفريش علشان السودوكو يرجع لاصله
def reset_grid(cells, grid, original_grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            cells[i][j].config(
                state="normal"
            )  # هنا بخلي الاماكن الي كنت كاتب فيها تبقي فاضيه وينفع اكتب فيها عادي
            cells[i][j].delete(0, tk.END)
            if (
                original_grid[i][j] != 0
            ):  # هنا بشوف هل المكان ده كان موجود فيه ارقام ولا هو كان فاضي وانا الي حطيت رقم
                cells[i][j].insert(0, str(original_grid[i][j]))
                cells[i][j].config(
                    state="disabled"
                )  # الاماكن الي كان فيها ارقام اصلا بثبتها


# --- Genetic Algorithm Section ---


# دالة لتوليد فرد عشوائي (حل عشوائي)
def generate_individual(size):
    return [
        [random.randint(1, size) if random.random() > 0.5 else 0 for _ in range(size)]
        for _ in range(size)
    ]


# دالة لتقييم مدى جودة الفرد (Fitness)
def fitness(board, solution):
    fitness_score = 0
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == solution[i][j]:
                fitness_score += 1
    return fitness_score


# دالة لتوليد الجيل الجديد من الأفراد
def crossover(parent1, parent2, size):
    child = [[0] * size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            child[i][j] = parent1[i][j] if random.random() > 0.5 else parent2[i][j]
    return child


# mutate دالة لإجراء عملية
def mutate(child, size):
    row, col = random.randint(0, size - 1), random.randint(0, size - 1)
    child[row][col] = random.randint(1, size)
    return child


# دي فانكشن الي بتحل السودوكو باستخدام الجينيتك
def solve_sudoku_genetic(
    board, solution, population_size=100, generations=1000, mutation_rate=0.05
):
    size = len(board)
    population = [generate_individual(size) for _ in range(population_size)]
    best_solution = None
    best_fitness = 0

    for generation in range(generations):
        population.sort(key=lambda x: fitness(x, solution), reverse=True)
        best_solution = population[0]
        best_fitness = fitness(best_solution, solution)
        if best_fitness == size * size:
            break

        next_population = population[:2]  # نخلي أفضل فردين في الجيل القادم
        while len(next_population) < population_size:
            parent1, parent2 = random.sample(population[:20], 2)
            child = crossover(parent1, parent2, size)
            if random.random() < mutation_rate:
                child = mutate(child, size)
            next_population.append(child)

        population = next_population

    return best_solution


def display_grid_window(grid, solution):
    global cells
    size = len(grid)
    original_grid = [row[:] for row in grid]  # تخزين النسخة الأصلية من الشبكة
    new_window = tk.Toplevel(root)
    new_window.geometry("500x500")

    grid_frame = tk.Frame(new_window)
    grid_frame.pack(side="top", expand=True, fill="both")

    cells = [
        [
            tk.Entry(grid_frame, width=5, font=("Arial", 25), justify="center")
            for _ in range(size)
        ]
        for _ in range(size)
    ]
    for i in range(size):
        for j in range(size):
            cells[i][j].grid(row=i, column=j, sticky="nsew")
            if grid[i][j] != 0:
                cells[i][j].insert(0, str(grid[i][j]))
                cells[i][j].config(state="disabled")

    grid_frame.grid_columnconfigure(list(range(size)), weight=1)
    grid_frame.grid_rowconfigure(list(range(size)), weight=1)
"""
    def check_solution():
        user_solution = [[0] * size for _ in range(size)]
        is_correct = True

        for i in range(size):
            for j in range(size):
                value = cells[i][j].get()
                if value.isdigit():
                    user_solution[i][j] = int(value)
                else:
                    user_solution[i][j] = 0

                if user_solution[i][j] != solution[i][j]:
                    is_correct = False

        if is_correct:
            messagebox.showinfo(
                "Correct!", "Congratulations! Your solution is correct."
            )
        else:
            messagebox.showerror(
                "Incorrect!", "Oops! Your solution is incorrect. Try again."
            )
"""
def check_solution():
    user_solution = [[0] * size for _ in range(size)]
    is_correct = True

    for i in range(size):
        for j in range(size):
            value = cells[i][j].get()
            if value.isdigit():
                user_solution[i][j] = int(value)
            else:
                user_solution[i][j] = 0

            if user_solution[i][j] != solution[i][j]:
                is_correct = False
                cells[i][j].config(bg="red")  # Highlight incorrect cells
            else:
                cells[i][j].config(bg="white")

    if is_correct:
        messagebox.showinfo("Correct!", "Congratulations! Your solution is correct.")
    else:
        messagebox.showerror("Incorrect!", "Oops! Your solution is incorrect. Try again.")

    solve_button = tk.Button(
        new_window,
        text="Solve Step by Step with backtrack",
        height=2,
        width=20,
        font=("Arial", 10, "bold"),
        command=lambda: solve_sudoku_step_by_step(grid, cells, solve_button),
    )
    solve_button.pack(side="bottom", fill="x", expand=True)

    genetic_button = tk.Button(
        new_window,
        text="Solve with Genetic Algorithm",
        height=2,
        width=20,
        font=("Arial", 10, "bold"),
        command=lambda: solve_genetic(grid, solution),
    )
    genetic_button.pack(side="bottom", fill="x", expand=True)

    button_frame = tk.Frame(new_window)
    button_frame.pack(side="bottom", expand=True, fill="x")

    tk.Button(
        button_frame,
        text="Check Solution",
        height=2,
        width=20,
        font=("Arial", 10, "bold"),
        command=check_solution,
    ).pack(side="left", expand=True)
    tk.Button(
        button_frame,
        text="Refresh",
        height=2,
        width=10,
        font=("Arial", 10, "bold"),
        command=lambda: reset_grid(cells, grid, original_grid),
    ).pack(side="left", expand=True)


def solve_genetic(grid, solution):
    best_solution = solve_sudoku_genetic(grid, solution)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            cells[i][j].delete(0, tk.END)
            cells[i][j].insert(0, str(best_solution[i][j]))
            cells[i][j].config(state="disabled")


# دي الفانكشن الي هنكول بيها الفانكشنز الي عمبناها فوق علشان نبدا اللعبه
def start_game(size, filled_numbers=41):
    board = generate_sudoku(size, filled_numbers)
    solution = [row[:] for row in board]
    solve_sudoku_backtrack(solution)
    display_grid_window(board, solution)


# ده ال gui ي اخواتي الي هيظهر للي هيلعب انشاءالله
root = tk.Tk()
root.geometry("500x200")

label = tk.Label(root, text="Choose grid size", font=("Arial", 20, "bold"))
label.pack()

frame = tk.Frame(root)
frame.pack(side="bottom", expand=True)

tk.Button(
    frame,
    text="4 * 4",
    command=lambda: start_game(4, filled_numbers=10),
    height=2,
    width=10,
    font=("Arial", 10, "bold"),
).pack(side="left", expand=True)
tk.Button(
    frame,
    text="6 * 6",
    command=lambda: start_game(6, filled_numbers=18),
    height=2,
    width=10,
    font=("Arial", 10, "bold"),
).pack(side="left", expand=True)
tk.Button(
    frame,
    text="9 * 9",
    command=lambda: start_game(9, filled_numbers=41),
    height=2,
    width=10,
    font=("Arial", 10, "bold"),
).pack(side="left", expand=True)

root.mainloop()
