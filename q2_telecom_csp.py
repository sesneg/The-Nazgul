import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import copy


class Telecom_CSP_Solver:
    def __init__(self, mountains=None, grid_size=10, num_towers=8):
        self.grid_size  = grid_size
        self.num_towers = num_towers
        self.mountains  = set(mountains) if mountains else set()
        self.towers     = [f"T{i+1}" for i in range(num_towers)]

        # Initial domain: all non-mountain cells
        all_cells = [(r, c) for r in range(grid_size)
                             for c in range(grid_size)
                             if (r, c) not in self.mountains]
        self.initial_domains = {t: list(all_cells) for t in self.towers}

    def is_consistent(self, assignment, cell):
        """Return True if placing a new tower at 'cell' is consistent with existing assignment."""
        r, c = cell
        for placed_cell in assignment.values():
            pr, pc = placed_cell
            # same row or column
            if pr == r or pc == c:
                return False
            # adjacency (including diagonal) within 1 step
            if abs(pr - r) <= 1 and abs(pc - c) <= 1:
                return False
        return True

    def forward_check(self, domains, tower, cell):
        """Prune domains of unassigned towers after placing tower at cell."""
        new_domains = copy.deepcopy(domains)
        r, c = cell
        for other in self.towers:
            if other in new_domains:   # unassigned
                pruned = []
                for (pr, pc) in new_domains[other]:
                    if pr == r or pc == c:
                        continue
                    if abs(pr - r) <= 1 and abs(pc - c) <= 1:
                        continue
                    pruned.append((pr, pc))
                new_domains[other] = pruned
                if not pruned:
                    return None   # domain wipe-out
        return new_domains

    def select_unassigned(self, assignment, domains):
        """Choose the tower with the fewest remaining valid cells (MRV)."""
        unassigned = [t for t in self.towers if t not in assignment]
        return min(unassigned, key=lambda t: len(domains[t]))

    def backtrack(self, assignment, domains):
        if len(assignment) == self.num_towers:
            return assignment

        tower = self.select_unassigned(assignment, domains)

        for cell in list(domains[tower]):
            if self.is_consistent(assignment, cell):
                assignment[tower] = cell

                # remove tower from domains (it's now assigned)
                new_domains = {t: v for t, v in domains.items() if t != tower}
                new_domains = self.forward_check(new_domains, tower, cell)

                if new_domains is not None:
                    result = self.backtrack(assignment, new_domains)
                    if result is not None:
                        return result

                del assignment[tower]

        return None

    def solve(self):
        solution = self.backtrack({}, copy.deepcopy(self.initial_domains))
        return solution

    def visualise(self, solution, title="MTC 5G Tower Placement", filename="towers.png"):
        fig, ax = plt.subplots(figsize=(8, 8))
        gs = self.grid_size

        # background
        ax.set_facecolor('#f5f5f5')

        # grid lines
        for i in range(gs + 1):
            ax.axhline(i, color='gray', linewidth=0.5)
            ax.axvline(i, color='gray', linewidth=0.5)

        # mountain cells
        for (r, c) in self.mountains:
            ax.add_patch(plt.Rectangle((c, gs - 1 - r), 1, 1,
                                        color='#8B4513', zorder=2))
            ax.text(c + 0.5, gs - 1 - r + 0.5, 'M',
                    ha='center', va='center',
                    fontsize=11, fontweight='bold', color='white', zorder=3)

        # towers
        if solution:
            for name, (r, c) in solution.items():
                ax.add_patch(plt.Rectangle((c, gs - 1 - r), 1, 1,
                                            color='#1565C0', zorder=2))
                ax.text(c + 0.5, gs - 1 - r + 0.5, 'T',
                        ha='center', va='center',
                        fontsize=11, fontweight='bold', color='white', zorder=3)

        ax.set_xlim(0, gs)
        ax.set_ylim(0, gs)
        ax.set_xticks(range(gs))
        ax.set_yticks(range(gs))
        ax.set_xticklabels(range(gs))
        ax.set_yticklabels(range(gs - 1, -1, -1))
        ax.set_title(title, fontsize=13, fontweight='bold')

        legend = [
            mpatches.Patch(color='#1565C0', label='Tower (T)'),
            mpatches.Patch(color='#8B4513', label='Mountain (M)'),
        ]
        ax.legend(handles=legend, loc='upper right', fontsize=9)
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        plt.close()
        print(f"[Saved] {filename}")

# Test Scenarios
scenarios = {
    "Level1_Coastal": [(0,0),(1,1),(9,9)],
    "Level2_Highlands": [(2,2),(2,3),(3,2),(3,3),(7,8),(8,7),(8,8)],
    "Level3_Brandberg": [(0,5),(1,5),(2,5),(3,5),(4,5),
                          (5,0),(5,1),(5,2),(5,3),(5,4)],
}

if __name__ == "__main__":
    for name, mountains in scenarios.items():
        print(f"\n{'='*50}")
        print(f"Solving: {name}")
        solver = Telecom_CSP_Solver(mountains=mountains)
        solution = solver.solve()

        if solution:
            print(f"  Solution found:")
            for t, cell in sorted(solution.items()):
                print(f"    {t} → {cell}")
            solver.visualise(solution,
                             title=f"MTC Tower Placement – {name.replace('_',' ')}",
                             filename=f"towers_{name}.png")
        else:
            print("  No solution found.")
