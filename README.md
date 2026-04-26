Artificial Intelligence Assignment 1
Overview

This repository contains our group’s solutions for Artificial Intelligence Assignment 1 (ARI711S)

The assignment covers key Artificial Intelligence topics, including search algorithms, constraint satisfaction problems, adversarial search, and reinforcement learning. All solutions were implemented in Python and are organized into separate scripts, with a Jupyter Notebook provided for consolidated execution and presentation.

Detail	Information
Course	Artificial Intelligence (ARI711S)
Qualification	Bachelor of Computer Science (Software Development)
NQF Level	7
Due Date	26 April 2026 @ 23:59
Total Marks	100
Group Members
Name	Student Number	GitHub Username
Goerge Jeremia-224018000 
Willie Ndengu-224036270 
Grace Urikos-223051764 
David Hailume-223096709
Absalom Elindi-223077518
Project Structure
ARI711S_Assignment/
ARI711S_Assignment1.ipynb     # Main Jupyter notebook containing all solutions
q1_warehouse.py               # Question 1 – Warehouse search algorithms
 q2_telecom_csp.py             # Question 2 – Telecom tower CSP solver
tictactoe.py                  # Question 3 – Minimax Tic-Tac-Toe logic
runner.py                     # Question 3 – Tkinter GUI for gameplay
q4_gridworld_SARSA.py         # Question 4 – SARSA Gridworld MDP
 warehouse.txt                 # Warehouse layout input file
 warehouse_path_greedy.png     # Output – Greedy search visualisation
 warehouse_path_astar.png      # Output – A* search visualisation
 towers_Level1_Coastal.png     # Output – Level 1 tower placement
towers_Level2_Highlands.png   # Output – Level 2 tower placement
towers_Level3_Brandberg.png   # Output – Level 3 tower placement
gridworld_solution.png        # Output – Value function and policy
README.md                     # Project documentation
Questions Summary
Question 1 – Search Algorithms: Warehouse Logistics Bot (25 marks)

This task involves implementing informed search algorithms to guide an Automated Guided Vehicle (AGV) from a charging station (A) to a product bin (B) within a warehouse grid.

The following algorithms were implemented:

Greedy Best-First Search, which prioritises the heuristic function h(n), calculated as the Euclidean distance to the goal
A* Search, which uses the evaluation function f(n) = g(n) + h(n), combining path cost and heuristic

The output includes visual representations of the search process, highlighting walls, explored states, and the final path.

Question 2 – Optimisation: Telecommunication Tower Placement (25 marks)

This question models a Constraint Satisfaction Problem (CSP) to determine optimal placement of signal boosters on a 10×10 grid.

Constraints applied:

No two towers may share the same row or column
Towers must not be placed in adjacent cells, including diagonals
Towers cannot be placed on mountain terrain

Techniques used:

Backtracking search
Minimum Remaining Values (MRV) heuristic
Forward checking

The solution was tested across three different scenarios:

Level	Region	Difficulty
1	Coastal	Easy
2	Highlands	Medium
3	Brandberg	Hard
Question 3 – Adversarial Search: Tic-Tac-Toe (25 marks)

This section focuses on developing an AI agent for Tic-Tac-Toe using the Minimax algorithm with alpha-beta pruning.

Key features:

Full game logic implemented from scratch
Alpha-beta pruning for improved efficiency
Graphical user interface using Tkinter
Human plays as O, AI plays as X
The AI plays optimally, ensuring the best possible outcome (a draw at minimum)
Question 4 – MDPs: SARSA (25 marks)

This task implements the SARSA (State-Action-Reward-State-Action) algorithm in a 5×5 Gridworld environment.

Parameters used:

Parameter	Value
Discount factor (γ)	0.9
Exploration rate (ε)	0.1
Learning rate (α)	0.2
Episodes	5000

The solution computes the optimal value function and corresponding policy, which are visualised and compared with expected theoretical results.

How to Run
Prerequisites

Install the required Python libraries:

pip install matplotlib numpy jupyter
Running Individual Scripts
python q1_warehouse.py        # Generates search path visualisations
python q2_telecom_csp.py      # Generates tower placement results
python runner.py              # Launches Tic-Tac-Toe GUI
python q4_gridworld_SARSA.py  # Outputs value table and saves plot
Running the Notebook
jupyter notebook ARI711S_Assignment1.ipynb

Open the notebook and select “Run All Cells” to execute all solutions.

Technologies Used
Python 3.10+
Matplotlib (visualisation)
NumPy (numerical computations)
Tkinter (graphical user interface)
Jupyter Notebook (submission and demonstration)
License

This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
Namibia University of Science and Technology (NUST)
Faculty of Computing and Informatics
ARI711S Teaching Team
