import math
import sys
import puzzle as pz


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class AStarFrontier():
    def __init__(self):
        self.frontier = set()

    def add(self, node):
        self.frontier.add(node)
        # print(f'adding to frontier {node.state}')

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            min_cost = math.inf
            selected_node = None
            for node in self.frontier:
                if selected_node is None:
                    selected_node = node
                if node.action is not None:
                    node_cost = node.action[1][0] + node.action[1][1]
                    if node_cost < min_cost:
                        min_cost = node_cost
                        selected_node = node
            self.frontier.remove(selected_node)
            # print(f'Removing from frontier {pz.board_to_list(selected_node.state)} {selected_node.action}')
            return selected_node


class SearchAlgo():
    def __init__(self):
        self.explored = None
        self.num_explored = 0

    def solve(self, board):
        """Finds a solution to search problem, if one exists."""

        # Keep track of number of states explored
        self.num_explored = 0
        state = pz.board_to_tuple(board)

        # Initialize frontier to just the starting position
        start = Node(state, parent=None, action=None)
        frontier = AStarFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:
            # assert (self.num_explored < 8192)
            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1
            if self.num_explored % 100 == 0:
                print(f'Number explored: {self.num_explored}')
                print(f'Exploring ... cost,mhd={node.action[1]}')

            # If node is the goal, then we have a solution
            if pz.mhd(node.state) == 0:  # solved!
                print(f'Puzzle SOLVED {node.state}   {pz.board_to_list(node.parent.state)}')
                print(f'Number explored: {self.num_explored}')
                print(f'Exploring ... cost,mhd={node.action[1]}')
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action[0])
                    cells.append(node.action[1])
                    node = node.parent
                print(f'Actions backward: {actions}')
                print(f'cost,mhd backward: {cells}')

                actions.reverse()
                return actions

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action in pz.actions(node.state):
                new_board = pz.result(node.state, action)
                mhd = pz.mhd(new_board)
                if node.action is not None:
                    cost = node.action[1][0] + 1
                else:
                    cost = 1
                child_state = pz.board_to_tuple(new_board)
                if not frontier.contains_state(child_state) and child_state not in self.explored:
                    child = Node(state=child_state, parent=node, action=(action, (cost, mhd)))
                    frontier.add(child)
