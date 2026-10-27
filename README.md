🧠 Reversi (Othello) - Smart AI (Minimax)

An advanced Reversi (Othello) game made with Python and Pygame. The computer can think multiple moves ahead to beat you.

📖 About the Project

This project brings the classic Reversi game to the next level with a smart computer opponent. The AI does not play randomly. It looks 4 moves into the future using the Minimax Algorithm.

To make the AI think faster and avoid freezing the game, it uses a technique called Alpha-Beta Pruning. This allows the AI to skip bad moves without calculating them completely.

“There is difference between my reversi game and classic game . The main difference is in classic reversi when you make a move , that move needs to change at least change one color of piece but you either pc dont need to change color when they make a move . If the position you want to make move is not occipied you are free to move . “



✨ Features

Minimax Algorithm: The AI calculates future moves (up to 4 steps ahead) to choose the safest and most winning move.

Alpha-Beta Pruning: Makes the AI much faster by ignoring bad branches in the calculation tree.

Virtual Simulation (Make/Undo): The AI tests its moves on a fake board. It uses an "undo" function to quickly go back after testing, which saves computer memory.

Advanced Scoring: The AI decides its moves based on a score map and the total number of pieces it can control in the future.

!!! The pygame GUI was made by AI.!!!

🚀 How to Install and Run

Requirements:
You need to have Python 3.x and the Pygame library installed on your computer.

Install Pygame by running this command in your terminal:

pip install pygame


Start the advanced AI game:

python main_minimax_reverse.py


🧠 How Does the AI Think?

It creates a virtual copy of the real game board.

It finds all possible moves and tests them one by one in the future.

It assumes you (the player) will play your best move, and it tries to beat that.

It uses the "undo" function to clean up the virtual board after testing a move.

After checking thousands of options, it plays the move with the highest score on the real board.
