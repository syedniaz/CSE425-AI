from queue import PriorityQueue

class PuzzleSolver:
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

    def count_misplaced_tiles(self, state):
        count = 0
        for i in range(9):
            if state[i] != self.goal[i]:
                count += 1
        return count

    def solve_puzzle(self):
        frontier = PriorityQueue()
        frontier.put((0 + self.count_misplaced_tiles(self.start), 0, self.start))
        came_from = {}
        cost_so_far = {}
        came_from[self.start] = None
        cost_so_far[self.start] = 0

        while not frontier.empty():
            current = frontier.get()[2]

            if current == self.goal:
                break

            for i, j, move in [(0, -1, "LEFT"), (0, 1, "RIGHT"), (-1, 0, "UP"), (1, 0, "DOWN")]:
                new_x = current.index(-1) // 3 + i
                new_y = current.index(-1) % 3 + j
                if new_x >= 0 and new_x < 3 and new_y >= 0 and new_y < 3:
                    new_state = list(current)
                    index_blank = new_state.index(-1)
                    index_new = new_x * 3 + new_y
                    new_state[index_blank], new_state[index_new] = new_state[index_new], new_state[index_blank]
                    new_state = tuple(new_state)
                    new_cost = cost_so_far[current] + 1
                    if new_state not in cost_so_far or new_cost < cost_so_far[new_state]:
                        cost_so_far[new_state] = new_cost
                        priority = new_cost + self.count_misplaced_tiles(new_state)
                        frontier.put((priority, new_cost, new_state))
                        came_from[new_state] = (current, move)

        if self.goal not in came_from:
            return None  # No path found

        path = []
        current = self.goal
        while current != self.start:
            path.append(current)
            current, move = came_from[current]
            path.append(move)
        path.append(self.start)
        path.reverse()

        return path

start_state = (1, 4, 2, -1, 5, 3, 6, 7, 8)
goal_state = (1, 2, -1, 5, 4, 3, 6, 7, 8)

puzzle_solver = PuzzleSolver(start_state, goal_state)
solution_path = puzzle_solver.solve_puzzle()

if solution_path is None:
    print("NO PATH FOUND")
else:
    print("PATH FOUND")
    print("Moves:", " -> ".join(solution_path[1::2]))
    print("Path:")
    for state in solution_path[::2]:
        print(state[:3])
        print(state[3:6])
        print(state[6:])
        print()
