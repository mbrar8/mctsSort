import torch
import torch.nn as nn
import numpy as np
import copy
import math

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0.0
        self.swapVal = None       
        self.maxChildren = 0
        for i in range(len(state)):
            for j in range(i+1, len(state)):
                self.maxChildren += 1

    def is_terminal(self):
        return all(self.state[i] <= self.state[i+1] for i in range(len(self.state) - 1))


    def swap(self, i, j):
        self.state[i], self.state[j] = self.state[j], self.state[i]

    def expanded(self):
        print("Expansion check")
        print(f"Num children: {len(self.children)}")
        if len(self.children) == 0:
            return (0.0, None)
        if len(self.children) == self.maxChildren:
            return (1.0, None)
        

        while (True):
            i, j = np.random.randint(len(self.state), size=2)
            while i == j:
                j = np.random.randint(len(self.state))
        
            valid_permutation = True
            for child in self.children:
                s = {i, j}
                if s == child.swapVal:
                    valid_permuation = False

            if valid_permutation == True:
                child = Node(copy.deepcopy(self.state), self)
                child.swapVal = {i,j}
                child.swap(i, j)
                self.children.append(child)
                return (0.5, child)
                
def mcts(state, depth):
    state.visits += 1
    exp_ratio, new_child = state.expanded()
    print(f"Depth: {depth}")
    print(f"Current State: {state.state}")
    print(f"Expanded Ratio: {exp_ratio}")
    if exp_ratio == 1.0:
        next_state = UCB(state)
        depth += 1
        depth = mcts(next_state, depth)
    else:
        if exp_ratio > 0:
            next_state = expand(new_child)
            depth += 1
        else:
            next_state = state
        depth = random_playout(next_state, depth)
    if depth == 0:
        state.value += 1
    else:
        state.value += 1.0/depth
    return depth


def UCB(state):
    C = 0.7
    weights = []
    swap_vals = []
    for child in state.children:
        w = child.value + C * math.sqrt(math.log(state.visits) / child.visits)
        weights.append(w)
        swap_vals.append(child.swapVal)

    dist = [w / sum(weights) for w in weights]
    print(f"UCB wts: {dist}")
    print(f"Swap Vals: {swap_vals}")


    return state.children[np.random.choice(len(state.children), p=dist)]

def random_playout(state, depth):
    if state.is_terminal():
        print(f"Array sorted with depth: {depth}")
        return depth
    else:
        i, j = np.random.randint(len(state.state), size=2)
        while i == j:
            j = np.random.randint(len(state.state))

        child = Node(copy.deepcopy(state.state), state)
        child.swapVal = {i,j}
        child.swap(i, j)
        child = expand(child)
        state.children.append(child)
        return random_playout(child, depth+1)

def expand(state):
    state.visits = 1
    state.value = 0
    return state



size = 3
limit = 100
state = np.random.randint(limit, size=size)
iterations = 10
root = Node(state)
for _ in range(iterations):
    mcts(root, 0)
