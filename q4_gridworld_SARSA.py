"""
gridworld_SARSA.py  –  SARSA (on-policy TD) for the 5×5 Gridworld MDP
Matches the textbook example: special states A=(0,1)→A'=(4,1)+10
                                              B=(0,3)→B'=(2,3)+5
γ=0.9, ε=0.1, α=0.2, episodes=5000
"""
import numpy as np
import random


class Gridworld:
    ACTIONS      = ['north', 'south', 'east', 'west']
    ACTION_DELTA = {'north': (-1, 0), 'south': (1, 0),
                    'east':  (0,  1), 'west':  (0, -1)}
    ARROW        = {'north': '↑', 'south': '↓', 'east': '→', 'west': '←'}

    def __init__(self, rows=5, cols=5):
        self.rows = rows
        self.cols = cols

        # Special states (row, col)
        self.special_states = {'A': (0, 1), 'B': (0, 3)}
        self.next_states    = {'A\'': (4, 1), 'B\'': (2, 3)}
        self.special_rewards = {'A': 10, 'B': 5}

        print("Initializing Gridworld...")
        print(f"Grid size: {rows}x{cols}")
        print(f"Special_states = {{'A': {self.special_states['A']}, 'B': {self.special_states['B']}}}")
        a_prime = self.next_states["A'"]
        b_prime = self.next_states["B'"]
        print(f"Next_to_states = {{\"A'\": {a_prime}, \"B'\": {b_prime}}}")
        print(f"Special_rewards = {{'A': {self.special_rewards['A']}, 'B': {self.special_rewards['B']}}}")

    def step(self, state, action):
        r, c = state
        # Special teleport states
        if state == self.special_states['A']:
            return self.next_states["A'"], self.special_rewards['A']
        if state == self.special_states['B']:
            return self.next_states["B'"], self.special_rewards['B']

        dr, dc = self.ACTION_DELTA[action]
        nr, nc = r + dr, c + dc
        if 0 <= nr < self.rows and 0 <= nc < self.cols:
            return (nr, nc), 0
        else:
            return state, -1   # hit wall

    def all_states(self):
        return [(r, c) for r in range(self.rows) for c in range(self.cols)]


def sarsa(env, gamma=0.9, epsilon=0.1, alpha=0.2, episodes=5000, steps=5000):
    # Q-table initialised to zero
    Q = {(s, a): 0.0
         for s in env.all_states()
         for a in env.ACTIONS}

    def epsilon_greedy(state):
        if random.random() < epsilon:
            return random.choice(env.ACTIONS)
        q_vals = [Q[(state, a)] for a in env.ACTIONS]
        return env.ACTIONS[int(np.argmax(q_vals))]

    print(f"\nStarting Q-learning with parameters:")
    print(f"γ = {gamma}")
    print(f" ε = {epsilon}")
    print(f" α = {alpha}")
    print(f" Episodes = {episodes}")
    print(f" Steps = {steps}")

    all_s = env.all_states()
    for ep in range(episodes):
        state  = all_s[ep % len(all_s)]
        action = epsilon_greedy(state)
        for _ in range(min(steps, 300)):
            next_state, reward = env.step(state, action)
            next_action        = epsilon_greedy(next_state)
            Q[(state, action)] += alpha * (
                reward + gamma * Q[(next_state, next_action)] - Q[(state, action)]
            )
            state  = next_state
            action = next_action

    return Q


def extract_V_and_policy(env, Q):
    V      = {}
    policy = {}
    for s in env.all_states():
        q_vals  = {a: Q[(s, a)] for a in env.ACTIONS}
        best_a  = max(q_vals, key=q_vals.get)
        V[s]    = q_vals[best_a]
        policy[s] = best_a
    return V, policy


def print_V(env, V):
    print("\nOptimal Value Function:")
    for r in range(env.rows):
        row_str = "  ".join(f"{V[(r,c)]:5.2f}" for c in range(env.cols))
        print(row_str)

def print_policy(env, policy):
    print("\nOptimal Policy:")
    for r in range(env.rows):
        print("  " + "  ".join(f"{policy[(r,c)]:5s}" for c in range(env.cols)))

    print("\nOptimal Policy (arrows):")
    for r in range(env.rows):
        print("  " + "  ".join(env.ARROW[policy[(r,c)]] for c in range(env.cols)))


def visualise(env, V, policy, filename="gridworld_solution.png"):
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # ── Value function heatmap ──
    ax = axes[0]
    grid_V = np.array([[V[(r,c)] for c in range(env.cols)] for r in range(env.rows)])
    im = ax.imshow(grid_V, cmap='RdYlGn', aspect='equal')
    plt.colorbar(im, ax=ax, shrink=0.8)
    for r in range(env.rows):
        for c in range(env.cols):
            ax.text(c, r, f"{grid_V[r,c]:.1f}",
                    ha='center', va='center', fontsize=9, fontweight='bold')
    # mark special states
    for label, (r, c) in env.special_states.items():
        ax.add_patch(plt.Rectangle((c-0.5, r-0.5), 1, 1,
                                    fill=False, edgecolor='blue', lw=2))
    ax.set_title("Optimal Value Function  $V_*$", fontsize=13, fontweight='bold')
    ax.set_xticks(range(env.cols))
    ax.set_yticks(range(env.rows))

    # ── Policy arrows ──
    ax2 = axes[1]
    ax2.set_facecolor('#f5f5f5')
    arrow_map = {'north': (0,-0.35), 'south': (0,0.35),
                 'east':  (0.35, 0), 'west':  (-0.35, 0)}
    for r in range(env.rows):
        for c in range(env.cols):
            a  = policy[(r, c)]
            dx, dy = arrow_map[a]
            ax2.annotate("", xy=(c + dx, r + dy), xytext=(c, r),
                         arrowprops=dict(arrowstyle="->", color='#1565C0', lw=1.5))

    for label, (r, c) in env.special_states.items():
        ax2.text(c, r - 0.42, label, ha='center', va='center',
                 fontsize=9, color='darkred', fontweight='bold')

    ax2.set_xlim(-0.5, env.cols - 0.5)
    ax2.set_ylim(-0.5, env.rows - 0.5)
    ax2.set_xticks(range(env.cols))
    ax2.set_yticks(range(env.rows))
    ax2.invert_yaxis()
    ax2.grid(True, color='gray', linewidth=0.5)
    ax2.set_title("Optimal Policy  $\\pi_*$", fontsize=13, fontweight='bold')

    plt.suptitle("SARSA Gridworld Solution  (γ=0.9, ε=0.1, α=0.2)", fontsize=14)
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[Saved] {filename}")


# Main

if __name__ == "__main__":
    env = Gridworld()

    Q = sarsa(env, gamma=0.9, epsilon=0.1, alpha=0.2,
              episodes=5000, steps=5000)

    print("\nEvaluating optimal value function and policy...")
    V, policy = extract_V_and_policy(env, Q)

    print_V(env, V)
    print_policy(env, policy)
    visualise(env, V, policy)
