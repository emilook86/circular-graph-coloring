def greedy_bfs_circular_chromatic_number(n, m, edges, K):
    """
    Greedy-BFS (k,d)-fixed approximation of the circular chromatic number chi_c(G).

    Parameters
    ----------
    n     : number of vertices (0, 1, ..., n-1)
    m     : number of edges
    edges : list of (i, j) tuples with i < j, one entry per edge
    K     : hyperparameter, maximum numerator to try

    Returns
    -------
    best_k        : numerator   of the best (k,d)-coloring found
    best_d        : denominator of the best (k,d)-coloring found
    final_coloring: list of length n with the assigned colors
    """

    # if no edges, then chi_c = 1
    if m == 0:
        return 1, 1, [0] * n

    # adjacency list for efficiency reasons
    adj = [[] for _ in range(n)]
    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)

    chi_c = float('inf')
    best_k = None
    best_d = None
    final_coloring = [None] * n

    for k in range(1, K + 1):
        for d in range(1, k + 1):
            colors = [-1] * n   # UNCOLORED
            valid = True

            def find_min_valid_color(u):
                c = 0
                while True:
                    valid = True
                    for w in adj[u]:
                        if colors[w] == -1:
                            continue
                        absdiff = abs(colors[w] - c)
                        if absdiff < d or absdiff > k - d:
                            valid = False
                            break

                    if valid:
                        return c
                    c += 1
                    if c >= k:
                        return None   # equivalent to "FAIL" in documentation

            while any(c == -1 for c in colors) and valid:
                v1 = min(i for i in range(n) if colors[i] == -1)
                colors[v1] = 0
                frontier = [v1]

                while frontier and valid:
                    new_frontier = [] # it is a list, since we only add once noncolored vertices
                    for v in frontier:
                        for u in adj[v]:
                            if colors[u] == -1:
                                c = find_min_valid_color(u)
                                if c is None:   # equivalent to "FAIL" in documentation
                                    valid = False
                                    break
                                colors[u] = c
                                new_frontier.append(u)
                    frontier = new_frontier

            if valid:
                ratio = k / d
                if ratio < chi_c:
                    chi_c = ratio
                    final_coloring = colors
                    best_k = k
                    best_d = d

    return best_k, best_d, final_coloring