"""
============================================================
  A* (A-Star) Search Algorithm
============================================================
  A* is a best-first search algorithm that finds the
  shortest path between two nodes in a graph. It uses a
  heuristic function to estimate the cost from the current
  node to the goal, making it more efficient than Dijkstra's.

  Formula: f(n) = g(n) + h(n)
    - g(n): actual cost from start to node n
    - h(n): heuristic estimate from n to goal
    - f(n): total estimated cost
============================================================
"""

import heapq

# ─────────────────────────────────────────────
# EXAMPLE 1: Grid Maze Pathfinding
# Find the shortest path through a grid maze
# 0 = open, 1 = wall
# ─────────────────────────────────────────────

def astar_grid(grid, start, goal):
    rows, cols = len(grid), len(grid[0])

    def heuristic(a, b):
        # Manhattan distance heuristic
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        neighbors = [
            (current[0]-1, current[1]),
            (current[0]+1, current[1]),
            (current[0],   current[1]-1),
            (current[0],   current[1]+1),
        ]

        for neighbor in neighbors:
            r, c = neighbor
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] == 0:
                tentative_g = g_score[current] + 1

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found


def print_grid_path(grid, path):
    display = [row[:] for row in grid]
    for r, c in path:
        display[r][c] = '*'
    sr, sc = path[0]
    er, ec = path[-1]
    display[sr][sc] = 'S'
    display[er][ec] = 'G'

    print("\n  Grid Legend: S=Start, G=Goal, *=Path, 1=Wall, 0=Open\n")
    for row in display:
        print("  " + " ".join(str(cell) for cell in row))


print("=" * 55)
print("  A* ALGORITHM — EXAMPLE 1: Grid Maze Pathfinding")
print("=" * 55)

maze = [
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0],
]

start = (0, 0)
goal  = (4, 4)
path  = astar_grid(maze, start, goal)

if path:
    print(f"\n  Start: {start}  →  Goal: {goal}")
    print(f"  Path found ({len(path)} steps): {path}")
    print_grid_path(maze, path)
else:
    print("  No path found.")


# ─────────────────────────────────────────────
# EXAMPLE 2: City Map — Weighted Graph
# Find shortest route between cities using
# road distances as edge weights
# ─────────────────────────────────────────────

def astar_graph(graph, heuristics, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], g_score[goal]

        for neighbor, weight in graph.get(current, []):
            tentative_g = g_score[current] + weight

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristics.get(neighbor, 0)
                heapq.heappush(open_set, (f, neighbor))

    return None, float('inf')


# Graph: city → [(neighbor, distance_km)]
city_graph = {
    "Manila":   [("Calamba", 54), ("Bulacan", 40)],
    "Calamba":  [("Manila", 54),  ("Lucena", 98), ("Batangas", 48)],
    "Bulacan":  [("Manila", 40),  ("Pampanga", 60)],
    "Lucena":   [("Calamba", 98), ("Naga", 194)],
    "Batangas": [("Calamba", 48), ("Naga", 240)],
    "Pampanga": [("Bulacan", 60), ("Dagupan", 120)],
    "Dagupan":  [("Pampanga", 120)],
    "Naga":     [("Lucena", 194), ("Batangas", 240), ("Legazpi", 109)],
    "Legazpi":  [("Naga", 109)],
}

# Straight-line distance estimates to "Legazpi" (heuristic)
heuristics_to_legazpi = {
    "Manila":   480,
    "Calamba":  420,
    "Bulacan":  500,
    "Lucena":   280,
    "Batangas": 370,
    "Pampanga": 560,
    "Dagupan":  670,
    "Naga":     109,
    "Legazpi":  0,
}

print("\n" + "=" * 55)
print("  A* ALGORITHM — EXAMPLE 2: City Route Finder")
print("=" * 55)

start_city = "Manila"
goal_city  = "Legazpi"
route, total_km = astar_graph(city_graph, heuristics_to_legazpi, start_city, goal_city)

if route:
    print(f"\n  Start: {start_city}  →  Goal: {goal_city}")
    print(f"  Shortest Route: {' → '.join(route)}")
    print(f"  Total Distance: {total_km} km")
else:
    print("  No route found.")

print("\n  Done! A* successfully found optimal paths in both examples.")
