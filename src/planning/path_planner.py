import heapq


class AStarPlanner:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.open_set = []
        self.closed_set = set()
        self.came_from = {}
        self.g_score = {self.start: 0}
        self.f_score = {self.start: self.heuristic(self.start)}
        heapq.heappush(self.open_set, (self.f_score[self.start], self.start))

    def heuristic(self, node):
        return abs(node[0] - self.goal[0]) + abs(node[1] - self.goal[1])

    def reconstruct_path(self, current):
        total_path = [current]
        while current in self.came_from:
            current = self.came_from[current]
            total_path.append(current)
        return total_path[::-1]

    def plan_path(self):
        while self.open_set:
            current = heapq.heappop(self.open_set)[1]

            if current == self.goal:
                return self.reconstruct_path(current)

            self.closed_set.add(current)
            neighbors = self.get_neighbors(current)

            for neighbor in neighbors:
                if neighbor in self.closed_set:
                    continue

                tentative_g_score = self.g_score[current] + 1  # assuming cost from current to neighbor is always 1

                if neighbor not in self.g_score or tentative_g_score < self.g_score[neighbor]:
                    self.came_from[neighbor] = current
                    self.g_score[neighbor] = tentative_g_score
                    self.f_score[neighbor] = self.g_score[neighbor] + self.heuristic(neighbor)
                    heapq.heappush(self.open_set, (self.f_score[neighbor], neighbor))

        return []

    def get_neighbors(self, node):
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 4-connected grid
        for direction in directions:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if 0 <= neighbor[0] < len(self.grid) and 0 <= neighbor[1] < len(self.grid[0]):
                if self.grid[neighbor[0]][neighbor[1]] == 0:  # assuming 0 is a free space and 1 is an obstacle
                    neighbors.append(neighbor)
        return neighbors


# Example usage:
if __name__ == "__main__":
    grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    start = (0, 0)
    goal = (4, 4)
    planner = AStarPlanner(grid, start, goal)
    path = planner.plan_path()
    print(f"Path: {path}")
