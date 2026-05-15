"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Zachary Welch
Student ID:   827470079

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        "Your Part 1 README answers, written as a string."
        Must match what you wrote in README Part 1.
    """
    return (
    "A single path run ignores relic chambers and the order where relics are collected.\n"
    "The order of visiting the chambers.\n"
    "The total cost depends on the visitation sequence, making it a ordering problem.\n"
    )


# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    sources = {spawn, exit_node}
    for r in relics:
        sources.add(r)
    return list(sources)


def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').
    """
    dist = {node: float('inf') for node in graph}
    dist[source] = 0
    pq = [(0, source)]
    while pq:
        current_dist, u = heapq.heappop(pq)
        if current_dist > dist[u]:
            continue
        for v, cost in graph.get(u, []):
            new_dist = current_dist + cost
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pq, (new_dist, v))
    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups for every source u
        your design requires.
    """
    sources = select_sources(spawn, relics, exit_node)
    dist_table = {}
    for src in sources:
        dist_table[src] = run_dijkstra(graph, src)
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.

    """
    return (
    "The source has distance 0, so its always correct there.\n"
    "All edge weights are nonnegative, so alternative paths can't produce a smaller value in a non finalized node.\n"
    "All nodes are finalized, so every stored distance is true.\n" 
    )


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.
    """
    return (
    "**The failure mode:** Greedy selection \n"
    "**Counter-example setup:** Visiting one relic might make the other relics harder to get to\n"
    "**What greedy picks:** Relic with the smallest travel cost\n" 
    "**What optimal picks:** Whatever pathway reduces present and future fuel costs the most\n"
    "**Why greedy loses:** Greedys current choices could undermine its overall cost.\n" 
    "The algorithm must explore different orders of how to visit relics.\n" 
    )



# =============================================================================
# PARTS 5 + 6
# =============================================================================

def find_optimal_route(dist_table, spawn, relics, exit_node):
    current_loc = spawn
    relics_remaining = set(relics)
    relics_visited_order = []
    cost_so_far = 0

    best = [float('inf'), []]

    _explore(dist_table, current_loc, relics_remaining,
             relics_visited_order, cost_so_far,
             exit_node, best)

    return tuple(best)


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):

    
    if not relics_remaining:
        exit_cost = dist_table[current_loc].get(exit_node, float('inf'))
        if exit_cost == float('inf'):
            return
        total_cost = cost_so_far + exit_cost
        if total_cost < best[0]:
            best[0] = total_cost
            best[1] = list(relics_visited_order)
        return

    
    min_to_relic = float('inf')
    for r in relics_remaining:
        d = dist_table[current_loc].get(r, float('inf'))
        min_to_relic = min(min_to_relic, d)

    min_to_exit = min(
        dist_table[r].get(exit_node, float('inf'))
        for r in relics_remaining
    )

    lower_bound = cost_so_far + min_to_relic + min_to_exit

# Pruning is safe because if the lower bound is allready the best, The branch is already complete
    if lower_bound >= best[0]:
        return

    

    for r in list(relics_remaining):
        travel_cost = dist_table[current_loc].get(r, float('inf'))
        if travel_cost == float('inf'):
            continue

        relics_remaining.remove(r)
        relics_visited_order.append(r)

        _explore(dist_table, r, relics_remaining,
                 relics_visited_order,
                 cost_so_far + travel_cost,
                 exit_node, best)

        relics_remaining.add(r)
        relics_visited_order.pop()



# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    dist_table = precompute_distances(graph, spawn, relics, exit_node)
    return find_optimal_route(dist_table, spawn, relics, exit_node)


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
