import random,math
import numpy as np
from functools import lru_cache
from Utils_and_visual_look.Utility_functions import *

C = 20
MID_GAME_THRESHOLD = 5
RANDOMNESS_THRESHOLD = 0.1
LEARNING_MULTIPLIER = 0.15

WINING_REWARD = 1000
LOSING_REWARD = -2100
BLOCKING_REWARD = 60
STACKING_REWARD = 5
PLAYING_MIDDLE_REWARD = 1

class MCTSAgent:
    
    def __init__(self, num_iterations, ROW_COUNT, COLUMN_COUNT,player):
        self.num_iterations = num_iterations
        self.ROW_COUNT = ROW_COUNT
        self.COLUMN_COUNT = COLUMN_COUNT
        self.heuristic_cache = {}
        # Which player this agent represents, player1 or 2
        self.player = player
    
    # Get all valid columns to place a piece
    def get_possible_actions(self, board):
        return list({i for i in range(self.COLUMN_COUNT) for j in range(self.ROW_COUNT) if board[j][i] == 0})
    
    # Function to get the next available row in a column
    def get_next_open_row(self, board, col):
        for r in range(self.ROW_COUNT):
            if board[r][col] == 0:
                return r
        return -1  # Return -1 if the column is full
    
    # Node for game tree
    class Node:
        def __init__(self, state, player, parent=None):
            self.state = state
            self.player = player
            self.visits = 0
            self.score = 0
            self.children = []
            self.parent = parent

        def __str__(self):
            return f"State:\n{self.state}\nPlayer: {self.player}\nVisits: {self.visits}\nscore: {self.score}\n"
        
        # UCB1 value of node (we calculate the Upper confidence bound for a selected node)
        def ucb1_value(self):
            return (self.score/self.visits) + C * math.sqrt(math.log(self.parent.visits)/self.visits)
        
    # Returns the best child from list
    def best_child_from_list(self, node):
        return max(node.children, key=lambda child: child.ucb1_value())
    
    # Count moves played
    def count_moves_played(self,board):
        return np.count_nonzero(board)
    
    # Check if the heuristic value for the current board state is cached
    @lru_cache(maxsize=128)
    def compute_heuristic(self, board_state):
       if board_state in self.heuristic_cache:
           return self.heuristic_cache[board_state]
       return None
   
    # Function for getting next borad
    def get_next_board(self,board, action, player):
        next_board = np.copy(board)
        next_row = self.get_next_open_row(next_board, action)
        if next_row != -1:
            next_board[next_row][action] = player
        return next_board
    
    # Function for winning moves
    def favor_winning_moves(self, board, action, current_player):
        next_board = self.get_next_board(board, action, current_player)
        if winning_move(next_board, current_player):
            return WINING_REWARD  # Adjust as needed
        return 0
    
    # Function for blocking moves
    def favor_blocking_moves(self, board, action, current_player):
        opponent = 1 if current_player == 2 else 2
        next_board_opponent = self.get_next_board(board, action, opponent)
        if winning_move(next_board_opponent, current_player):
            return BLOCKING_REWARD  # Adjust as needed
        return 0
    
    # Function for stacking moves
    def favor_stacking(self,board, action):
        vertical_height = np.count_nonzero(board[:, action])  # Count pieces in the column
        if vertical_height > 1:  # Favor stacking
            return STACKING_REWARD
        return 0
    
    # Function for avoiding losing moves
    def avoid_losing_moves(self, board, action, current_player):
        opponent = 1 if current_player == 2 else 2
        next_board = self.get_next_board(board, action, current_player)
        if winning_move(next_board, current_player):
           return LOSING_REWARD  # Avoid immediate loss
        return 0

    # Heuristic function
    def apply_dynamic_heuristic(self, board, possible_actions, current_player):
        heuristic_values = [1, 4, 5, 7, 5, 4, 1]  # Initial heuristic values (center columns get a higher score)
        center_columns = [2, 3, 4]  # Columns 2, 3 and 4 are the center columns

        if self.count_moves_played(board) >= MID_GAME_THRESHOLD:
            for action in possible_actions:
                next_board = self.get_next_board(board, action, current_player)
                board_state = tuple(map(tuple, next_board))
                heuristic_value = self.compute_heuristic(board_state)  # Use cached value if available
                if heuristic_value is None:
                    if action in center_columns:
                        heuristic_values[action] += PLAYING_MIDDLE_REWARD  # Slight increase for center columns
                    heuristic_values[action] += self.favor_winning_moves(board, action, current_player)
                    heuristic_values[action] += self.favor_blocking_moves(board, action, current_player)
                    heuristic_values[action] += self.favor_stacking(board, action)
                    heuristic_values[action] += self.avoid_losing_moves(board, action, current_player)
                    # Store calculated heuristic value in the cache
                    self.heuristic_cache[board_state] = heuristic_values[action]

        return [heuristic_values[col] for col in possible_actions]
    
    # Expand a node - by generating ALL POSSIBLE child nodes (next states)
    # Each child represents a potential new game state
    def node_expansion(self, node):
        possible_actions = self.get_possible_actions(node.state)
        heuristic_values = self.apply_dynamic_heuristic(node.state, possible_actions, node.player)

        # Create child nodes for each valid action, and add them to CHILDREN list
        for idx, action in enumerate(possible_actions):
            new_board = np.copy(node.state)
            new_board[self.get_next_open_row(new_board, action)][action] = node.player
            new_node = self.Node(new_board, 1 if node.player == 2 else 2, node)
            node.children.append(new_node)
            new_node.score = heuristic_values[idx]
    
    # Make some strategic moves
    def get_strategic_moves(self, board, current_player):
        strategic_moves = []

        for col in range(self.COLUMN_COUNT):
            row = self.get_next_open_row(board, col)
            if row != -1:
                # Prioritize stacking, sequence building, and winning moves
                if row > 0 and board[row - 1][col] == current_player:
                    strategic_moves.append(col)
                elif row == 0:
                    strategic_moves.append(col)  # Consider stacking for an empty column

                # Check if the move leads to a win for the current player
                next_board = np.copy(board)
                next_board[row][col] = current_player
                if winning_move(next_board, current_player):
                    strategic_moves.append(col)  # Collect winning move
        return strategic_moves

    # Simulate a random game from the CURRENT NODE -> to the END
    def simulation(self, node):
        current_player = node.player
        simulation_board = np.copy(node.state)
        actions = self.get_possible_actions(simulation_board)

        for _ in range(len(actions)):  # Perform moves equal to the total available actions
            if winning_move(simulation_board, current_player):
                # Return score based on the current player's perspective
                return WINING_REWARD if current_player == self.player else LOSING_REWARD

            # Randomly prioritize intelligent moves in a constrained manner
            if np.random.rand() > RANDOMNESS_THRESHOLD:
                # Intelligent move: prioritize stacking or strategic moves
                strategic_moves = self.get_strategic_moves(simulation_board, current_player)
                if strategic_moves:
                    action = random.choice(strategic_moves)
                else:
                    action = random.choice(actions)
            else:
                action = random.choice(actions)  # Random move
            simulation_board[self.get_next_open_row(simulation_board, action)][action] = current_player
            current_player = 1 if current_player == 2 else 2
            actions = self.get_possible_actions(simulation_board)

        return 0
    
    # Find the best column. Identifies the column corresponding to the best move by comparing the root state and the best child state
    def find_best_column(self, current_state, best_state):
        for col in range(len(current_state[0])):
            for row in range(len(current_state)):
                if current_state[row][col] != best_state[row][col]:
                    return col
        return -1       
    
    # Updated cache update method
    def update_cache(self, node):
        state_key = tuple(map(tuple, node.state))
        if state_key in self.heuristic_cache and np.random.rand() > RANDOMNESS_THRESHOLD:  # Controlled randomness
            # Update cache based on a multiplier of the difference in scores
            self.heuristic_cache[state_key] = (node.score - self.heuristic_cache[state_key]) * LEARNING_MULTIPLIER  # Adjust multiplier as needed
        else:
            self.heuristic_cache[state_key] = node.score    # Randomly update some states (added randomness)
                     
    # MCTS core logic. It determines the best move for the CURRENT board
    def monte_carlo_tree_search(self, current_board):
        # Create a node to represent the current state of the board (and the current player)
        root = self.Node(current_board, self.player)
        self.node_expansion(root)

        # Perform a fixed number of MCTS iterations
        for _ in range(self.num_iterations):
            node = root
            # Select unvisited child nodes for exploration
            not_visited_children = [child for child in node.children if child.visits == 0]
            if not_visited_children:
                node = random.choice(not_visited_children)
            else:
                # all children have been visited, now we will select the BEST CHILD using the UBC1 formula, and expand it
                best_child = self.best_child_from_list(node)
                self.node_expansion(best_child)
                if not best_child.children:
                    break
                node = random.choice(best_child.children) # Get random child form best_child to Rollout

            # Simulate the game from the selected node - to determine the outcome
            simulation_result = self.simulation(node)

            # Backpropagation. Updates the scores and visit counts from the simulated node - back to the root
            parent_node = node
            while parent_node is not None:
                parent_node.visits += 1
                parent_node.score += simulation_result  # Update the score
                parent_node = parent_node.parent

            # Update heuristic cache for faster future lookups
            self.update_cache(node)

        best_node = self.best_child_from_list(root)
        # print(best_node)
        return self.find_best_column(root.state, best_node.state)