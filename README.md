# The Torchbearer

**Student Name:** Zachary Welch
**Student ID:** 827470079
**Course:** CS 460 – Algorithms | Spring 2026

> This README is your project documentation. Write it the way a developer would document
> their design decisions , bullet points, brief justifications, and concrete examples where
> required. You are not writing an essay. You are explaining what you built and why you built
> it that way. Delete all blockquotes like this one before submitting.

---

## Part 1: Problem Analysis

> Document why this problem is not just a shortest-path problem. Three bullet points, one
> per question. Each bullet should be 1-2 sentences max.

- **Why a single shortest-path run from S is not enough:**
  A single path run ignores relic chambers and the order where relics are collected.

- **What decision remains after all inter-location costs are known:**
  The order of visiting the chambers.

- **Why this requires a search over orders (one sentence):**
  The total cost depends on the visitation sequence, making it a ordering problem.
---

## Part 2: Precomputation Design

### Part 2a: Source Selection

> List the source node types as a bullet list. For each, one-line reason.

| Source Node Type | Why it is a source |
|---|---|
| spawn| We need to calculate the distance from the starting location to relics |
| relic node | We need to calculate the distance from one relic node to others |
| exit | Running it last just to make sure

### Part 2b: Distance Storage

> Fill in the table. No prose required.

| Property | Your answer |
|---|---|
| Data structure name | dist_table |
| What the keys represent | Outer represents source node where as inner represents destination |
| What the values represent | Fuel cost from source to destination |
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Hash table gives constant time access |

### Part 2c: Precomputation Complexity

> State the total complexity and show the arithmetic. Two to three lines max.

- **Number of Dijkstra runs:** k+2
- **Cost per run:** O(m log n)
- **Total complexity:** O((k+2)m log n)
- **Justification (one line):** We run Dijkstra once from spawn and once from each relic , and once from the exit

---

## Part 3: Algorithm Correctness

> Document your understanding of why Dijkstra produces correct distances.
> Bullet points and short sentences throughout. No paragraphs.

### Part 3a: What the Invariant Means

> Two bullets: one for finalized nodes, one for non-finalized nodes.
> Do not copy the invariant text from the spec.

- **For nodes already finalized (in S):**
  The stored distance is the true shortest path from the source

- **For nodes not yet finalized (not in S):**
  The stored distance is the shortest discovered path for the nodes that are finalized

### Part 3b: Why Each Phase Holds

> One to two bullets per phase. Maintenance must mention nonnegative edge weights.

- **Initialization : why the invariant holds before iteration 1:**
  The source has distance 0, so its always correct there.

- **Maintenance : why finalizing the min-dist node is always correct:**
  All edge weights are nonnegative, so alternative paths can't produce a smaller value in a non finalized node.

- **Termination : what the invariant guarantees when the algorithm ends:**
  All nodes are finalized, so every stored distance is true.

### Part 3c: Why This Matters for the Route Planner

> One sentence connecting correct distances to correct routing decisions.

If the route planner knows the distances are in fact correct it will compare accurate fuel costs when chosing relics. 

---

## Part 4: Search Design

### Why Greedy Fails

> State the failure mode. Then give a concrete counter-example using specific node names
> or costs (you may use the illustration example from the spec). Three to five bullets.

- **The failure mode:** Greedy selection
- **Counter-example setup:** Visiting one relic might make the other relics harder to get to
- **What greedy picks:** Relic with the smallest travel cost
- **What optimal picks:** Whatever pathway reduces present and future fuel costs the most
- **Why greedy loses:** Greedys current choices could undermine its overall cost.

### What the Algorithm Must Explore

> One bullet. Must use the word "order."

- The algorithm must explore different orders of how to visit relics.

---

## Part 5: State and Search Space

### Part 5a: State Representation

> Document the three components of your search state as a table.
> Variable names here must match exactly what you use in torchbearer.py.

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | | | |
| Relics already collected | | | |
| Fuel cost so far | | | |

### Part 5b: Data Structure for Visited Relics

> Fill in the table.

| Property | Your answer |
|---|---|
| Data structure chosen | |
| Operation: check if relic already collected | Time complexity: |
| Operation: mark a relic as collected | Time complexity: |
| Operation: unmark a relic (backtrack) | Time complexity: |
| Why this structure fits | |

### Part 5c: Worst-Case Search Space

> Two bullets.

- **Worst-case number of orders considered:** _Your answer (in terms of k)._
- **Why:** _One-line justification._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

> Three bullets.

- **What is tracked:** _Your answer here._
- **When it is used:** _Your answer here._
- **What it allows the algorithm to skip:** _Your answer here._

### Part 6b: Lower Bound Estimation

> Three bullets.

- **What information is available at the current state:** _Your answer here._
- **What the lower bound accounts for:** _Your answer here._
- **Why it never overestimates:** _Your answer here._

### Part 6c: Pruning Correctness

> One to two bullets. Explain why pruning is safe.

- _Your answer here._

---

## References

> Bullet list. If none beyond lecture notes, write that.

- _Your references here._
