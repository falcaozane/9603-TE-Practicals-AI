#ArunSanyal_9523_BatchA
#SolvingWaterJugProblemUsingBFS

from collections import deque

def water_jug_bfs(capacity_jug1, capacity_jug2, target):
    visited_states = set()
    queue = deque([(0, 0, "Initial State")])  # Initial state: both jugs are empty
    visited_states.add((0, 0))
    parent = {}  # Dictionary to keep track of the parent state for each state

    while queue:
        current_state = queue.popleft()
        jug1, jug2, action = current_state

        # Check if the goal state is reached
        if jug2 == target:
            print_steps(current_state, parent)
            return

        # Fill jug1
        fill_jug1 = (capacity_jug1, jug2, "Fill Jug1")
        if fill_jug1 not in visited_states:
            visited_states.add(fill_jug1)
            queue.append(fill_jug1)
            parent[fill_jug1] = current_state

        # Fill jug2
        fill_jug2 = (jug1, capacity_jug2, "Fill Jug2")
        if fill_jug2 not in visited_states:
            visited_states.add(fill_jug2)
            queue.append(fill_jug2)
            parent[fill_jug2] = current_state

        # Pour water from jug1 to jug2
        pour_jug1_to_jug2 = (max(0, jug1 - (capacity_jug2 - jug2)), min(jug2 + jug1, capacity_jug2), "Pour Jug1 to Jug2")
        if pour_jug1_to_jug2 not in visited_states:
            visited_states.add(pour_jug1_to_jug2)
            queue.append(pour_jug1_to_jug2)
            parent[pour_jug1_to_jug2] = current_state

        # Pour water from jug2 to jug1
        pour_jug2_to_jug1 = (min(jug1 + jug2, capacity_jug1), max(0, jug2 - (capacity_jug1 - jug1)), "Pour Jug2 to Jug1")
        if pour_jug2_to_jug1 not in visited_states:
            visited_states.add(pour_jug2_to_jug1)
            queue.append(pour_jug2_to_jug1)
            parent[pour_jug2_to_jug1] = current_state

        # Empty jug1
        empty_jug1 = (0, jug2, "Empty Jug1")
        if empty_jug1 not in visited_states:
            visited_states.add(empty_jug1)
            queue.append(empty_jug1)
            parent[empty_jug1] = current_state

        # Empty jug2
        empty_jug2 = (jug1, 0, "Empty Jug2")
        if empty_jug2 not in visited_states:
            visited_states.add(empty_jug2)
            queue.append(empty_jug2)
            parent[empty_jug2] = current_state

def print_steps(state, parent):
    steps = []
    while state[2] != "Initial State":
        steps.append(state)
        state = parent[state]
    steps.append((0, 0, "Initial State"))

    steps.reverse()
    for step in steps:
        print(f"{step[2]}: {step[0]} | {step[1]}")

# Example usage
capacity_jug1 = 3
capacity_jug2 = 4
target = 2

water_jug_bfs(capacity_jug1, capacity_jug2, target)



# Initial State: 0 | 0
# Fill Jug1: 3 | 0
# Pour Jug1 to Jug2: 0 | 3
# Fill Jug1: 3 | 3
# Pour Jug1 to Jug2: 2 | 4
# Empty Jug2: 2 | 0
# Pour Jug1 to Jug2: 0 | 2