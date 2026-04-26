import heapq
import math
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

class Node:
    def __init__(self, state, parent=None, action=None, g=0):
        self.state  = state   # (row, col)
        self.parent = parent
        self.action = action  # 'up','down','left','right'
        self.g      = g       # path cost so far

    def __lt__(self, other):
        return False          # tie-break for heapq


class Warehouse:
    def __init__(self, filepath):
        self.walls  = set()
        self.start  = None
        self.goal   = None
        self.grid   = []
        self._parse(filepath)

    def _parse(self, filepath):
        # If the file doesn't exist, create a sample warehouse for demo
        if not os.path.exists(filepath):
            print(f"[INFO] {filepath} not found – using built-in sample warehouse.")
            layout = [
                "####################",
                "#A   #    #    #   B#",
                "#    #    #    #    #",
                "#         #         #",
                "#    ###########    #",
                "#         #         #",
                "#    #    #    #    #",
                "#    #         #    #",
                "####################",
            ]
        else:
            with open(filepath) as f:
                layout = [line.rstrip('\n') for line in f]

        self.grid = layout
        for r, row in enumerate(layout):
            for c, ch in enumerate(row):
                if ch == '#':
                    self.walls.add((r, c))
                elif ch == 'A':
                    self.start = (r, c)
                elif ch == 'B':
                    self.goal  = (r, c)

        self.rows = len(layout)
        self.cols = max(len(row) for row in layout)
        assert self.start, "No 'A' found in warehouse layout"
        assert self.goal,  "No 'B' found in warehouse layout"

    def heuristic(self, state):
        x1, y1 = state
        x2, y2 = self.goal
        return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    def neighbors(self, state):
        r, c = state
        result = []
        for action, (dr, dc) in [('up',(-1,0)),('down',(1,0)),
                                   ('left',(0,-1)),('right',(0,1))]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols \
               and (nr, nc) not in self.walls:
                result.append((action, (nr, nc)))
        return result

    def solve(self, algorithm="astar"):
        start_node = Node(self.start, g=0)
        h0 = self.heuristic(self.start)
        priority = h0 if algorithm == "greedy" else 0 + h0

        frontier  = []
        heapq.heappush(frontier, (priority, start_node))

        explored   = set()
        frontier_states = {self.start}

       while frontier: 
           _, node = heapq.heappop(frontier)
           frontier_states.discard(node.state)
    if node.state == self.goal:
        return self._extract_path(node), explored 
        if node.state in explored:
            continue
            explored.add(node.state) 
            for action, next_state in self.neighbors(node.state):
                if next_state not in explored and next_state not in frontier_states:
                    g_new = node.g + 1 
                    h_new = self.heuristic(next_state)
                    p_new = h_new if algorithm == "greedy" else g_new + h_new
                    child = Node(next_state, parent=node, action=action, g=g_new) 
                    heapq.heappush(frontier, (p_new, child))
                    frontier_states.add(next_state)
                    
                    return None, explored # no path found

    def _extract_path(self, node):
        path = []
        while node.parent:
            path.append(node.state)
            node = node.parent
        path.append(self.start)
        path.reverse()
        return path

    def visualise(self, path, explored, filename="warehouse_path.png", title=""):
        path_set = set(path)
        img = np.ones((self.rows, self.cols, 3))

        color_map = {
            'wall':     [0.2, 0.2, 0.2],   # dark gray
            'explored': [0.8, 0.9, 1.0],   # light blue
            'path':     [0.0, 0.8, 0.0],   # green
            'start':    [1.0, 0.6, 0.0],   # orange
            'goal':     [1.0, 0.1, 0.1],   # red
            'open':     [1.0, 1.0, 1.0],   # white
        }

        for r in range(self.rows):
            for c in range(self.cols):
                state = (r, c)
                if state in self.walls:
                    img[r, c] = color_map['wall']
                elif state == self.start:
                    img[r, c] = color_map['start']
                elif state == self.goal:
                    img[r, c] = color_map['goal']
                elif state in path_set:
                    img[r, c] = color_map['path']
                elif state in explored:
                    img[r, c] = color_map['explored']

        fig, ax = plt.subplots(figsize=(max(8, self.cols * 0.5),
                                        max(6, self.rows * 0.5)))
        ax.imshow(img, interpolation='nearest')
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('off')

        legend = [
            mpatches.Patch(color=color_map['wall'],     label='Shelving (Wall)'),
            mpatches.Patch(color=color_map['path'],     label='Optimal Path'),
            mpatches.Patch(color=color_map['explored'], label='Explored'),
            mpatches.Patch(color=color_map['start'],    label='Charging Station (A)'),
            mpatches.Patch(color=color_map['goal'],     label='Product Bin (B)'),
        ]
        ax.legend(handles=legend, loc='upper right', fontsize=8,
                  bbox_to_anchor=(1.25, 1.0))
        plt.tight_layout()
        plt.savefig(filename, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"[Saved] {filename}")

if __name__ == "__main__":
    wh = Warehouse("warehouse.txt")

    for algo in ["greedy", "astar"]:
        path, explored = wh.solve(algorithm=algo)
        if path:
            print(f"\n[{algo.upper()}]")
            print(f"  Path length : {len(path)} cells")
            print(f"  Explored    : {len(explored)} states")
            print(f"  Path        : {path}")
            fname = f"warehouse_path_{algo}.png"
            wh.visualise(path, explored, filename=fname,
                         title=f"Warehouse – {algo.upper()} Search\n"
                               f"Path={len(path)} cells  |  Explored={len(explored)} states")
        else:
            print(f"[{algo.upper()}] No path found.")
