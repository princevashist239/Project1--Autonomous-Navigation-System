import heapq

def a_star(grid, start, goal):
    """Calculates the most efficient path avoiding obstacles[cite: 447, 505]."""
    rows, cols = grid.shape
    open_list = []
    heapq.heappush(open_list, (0, start))
    came_from = {}
    g_score = {start: 0}
    
    while open_list:
        current = heapq.heappop(open_list)[1]
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1] # Path found [cite: 509]
        
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
            neighbor = (current[0] + dr, current[1] + dc)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if grid[neighbor[0], neighbor[1]] == 1: continue
                
                # Diagonal movement cost is higher (1.41) than straight (1)
                weight = 1.41 if dr != 0 and dc != 0 else 1
                tentative_g = g_score[current] + weight
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + abs(neighbor[0]-goal[0]) + abs(neighbor[1]-goal[1])
                    heapq.heappush(open_list, (f_score, neighbor))
    return None