import random
import copy
import json

class SudokuPuzzleSolver:
    def __init__(self, grid):
        self.grid = grid
        self.grid_size = 9
        self.empty_cell_symbol = "0"  

    def is_move_valid(self, row, col, number):
        if number in self.grid[row]:
            return False
        if number in [self.grid[i][col] for i in range(self.grid_size)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] == number:
                    return False
        return True

    def find_next_empty(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j] == self.empty_cell_symbol:
                    return i, j
        return None

    def solve_puzzle(self):
        empty_position = self.find_next_empty()
        if not empty_position:
            return True  

        row, col = empty_position
        for number in map(str, range(1, 10)):
            if self.is_move_valid(row, col, number):
                self.grid[row][col] = number
                if self.solve_puzzle():
                    return True
                self.grid[row][col] = self.empty_cell_symbol 
        return False

    def display_grid(self):
        for row in self.grid:
            print(" ".join(row))

    def apply_genetic_algorithm(self, population_size=100, generations=500):
        population = [self._generate_candidate() for _ in range(population_size)]
        for generation in range(generations):
            population = sorted(population, key=self._fitness_score, reverse=True)
            if self._fitness_score(population[0]) == self.grid_size * 3:
                self.grid = population[0]
                return True
            next_population = population[:10]
            while len(next_population) < population_size:
                parent1, parent2 = random.choices(population[:30], k=2)
                child = self._crossover(parent1, parent2)
                if random.random() < 0.1:
                    self._mutate(child)
                next_population.append(child)
            population = next_population
        return False

    def _generate_candidate(self):
        candidate = copy.deepcopy(self.grid)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if candidate[i][j] == self.empty_cell_symbol:
                    candidate[i][j] = str(random.randint(1, 9))
        return candidate

    def _fitness_score(self, grid):
        score = 0
        for i in range(self.grid_size):
            if len(set(grid[i])) == self.grid_size:
                score += 1
            if len(set(row[i] for row in grid)) == self.grid_size:
                score += 1
        for i in range(0, self.grid_size, 3):
            for j in range(0, self.grid_size, 3):
                subgrid = [grid[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
                if len(set(subgrid)) == self.grid_size:
                    score += 1
        return score

    def _crossover(self, parent1, parent2):
        child = copy.deepcopy(parent1)
        for i in range(self.grid_size):
            if random.random() > 0.5:
                child[i] = parent2[i]
        return child

    def _mutate(self, grid):
        row, col = random.randint(0, 8), random.randint(0, 8)
        grid[row][col] = str(random.randint(1, 9))

with open('puzzles.json', 'r') as file:
    puzzles_data = json.load(file)

for index, puzzle_grid in enumerate(puzzles_data['puzzles']):
    print(f"\nSolving Puzzle {index + 1}...")
    solver = SudokuPuzzleSolver(puzzle_grid)
    if solver.solve_puzzle():
        print(f"Puzzle {index + 1} solved:")
        solver.display_grid()
    else:
        print(f"Puzzle {index + 1} could not be solved with backtracking. Applying genetic algorithm...")
        if solver.apply_genetic_algorithm():
            print(f"Puzzle {index + 1} solved with genetic algorithm:")
            solver.display_grid()
        else:
            print(f"Puzzle {index + 1} could not be solved.")
