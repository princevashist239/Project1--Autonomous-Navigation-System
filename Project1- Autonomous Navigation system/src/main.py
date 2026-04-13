import cv2
import numpy as np
import random
from src.planning import a_star

# Configuration [cite: 125, 497]
GRID_SIZE, CELL = 20, 30
WIDTH = GRID_SIZE * CELL

class DynamicObstacle:
    def __init__(self):
        self.r, self.c = random.randint(5, 15), random.randint(5, 15)
        self.dr, self.dc = random.choice([-1, 1]), random.choice([-1, 1])

    def update(self):
        if not (1 <= self.r + self.dr < GRID_SIZE - 1): self.dr *= -1
        if not (1 <= self.c + self.dc < GRID_SIZE - 1): self.dc *= -1
        self.r += self.dr
        self.c += self.dc

def run_navigation():
    agent, goal = (0, 0), (19, 19)
    obstacles = [DynamicObstacle() for _ in range(4)] # 4 Moving obstacles [cite: 297]
    
    print("Initializing Autonomous Navigation System...") # [cite: 195]

    while agent != goal:
        # 1. Perception: Scan the world [cite: 27, 499]
        grid = np.zeros((GRID_SIZE, GRID_SIZE))
        for obs in obstacles:
            obs.update()
            grid[obs.r, obs.c] = 1 # Mark obstacle [cite: 501]
        
        # 2. Path Planning: Re-calculate best route [cite: 33, 443]
        path = a_star(grid, agent, goal)
        
        # 3. Visualization: Industry-oriented Dashboard [cite: 89, 149]
        frame = np.ones((WIDTH, WIDTH, 3), dtype=np.uint8) * 255
        
        # Draw Obstacles (Red)
        for obs in obstacles:
            cv2.circle(frame, (obs.c*CELL+15, obs.r*CELL+15), 12, (0, 0, 255), -1)
        
        # Draw Path (Light Gray)
        if path:
            for p in path:
                cv2.rectangle(frame, (p[1]*CELL+10, p[0]*CELL+10), (p[1]*CELL+20, p[0]*CELL+20), (200, 200, 200), -1)
            agent = path[0] # Step forward [cite: 189]

        # Draw Agent (Blue) and Goal (Green)
        cv2.circle(frame, (agent[1]*CELL+15, agent[0]*CELL+15), 10, (250, 0, 0), -1)
        cv2.rectangle(frame, (goal[1]*CELL+5, goal[0]*CELL+5), (goal[1]*CELL+25, goal[0]*CELL+25), (0, 200, 0), 2)
        
        cv2.imshow("AI Navigation Dashboard", frame)
        if cv2.waitKey(150) & 0xFF == ord('q'): break

    print("Mission Complete: Goal Reached Safely!") # [cite: 192]
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_navigation()
