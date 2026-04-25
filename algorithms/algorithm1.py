def approximate_circular_chromatic_number(n, m, edges, D):
    """
    DFS-based approximation of the circular chromatic number chi_c(G).

    Parameters
    ----------
    n     : number of vertices (0, 1, ..., n-1)
    m     : number of edges
    edges : list of (i, j) tuples with i < j, one entry per edge
    D     : hyperparameter, maximum denominator to try

    Returns
    -------
    best_k        : numerator   of the best (k,d)-coloring found
    best_d        : denominator of the best (k,d)-coloring found
    final_coloring: list of length n with the assigned colors
    """

    # if no edges , then chi_c = 1
    if m == 0:
        return 1, 1, [0] * n
    
    # adjacency list for the efficiency reasons
    adj = [[] for _ in range(n)]
    for i, j in edges:
        adj[i].append(j)
        adj[j].append(i)

    chi_c = float('inf')
    best_k = None
    best_d = None
    final_coloring = [None] * n

    k = [2 * val for val in range(D + 1)]  # k[d] = 2d initially, also k[0] is unused

    for d in range(1, D + 1):
        colors  = [-1] * n   # UNCOLORED
        visited = [False] * n
        parent  = [-1] * n   # NULL

        def find_min_valid_color(u, p):
            c = 0
            k_lowest = k[d]

            while True:
                valid = True

                for w in adj[u]:    # easier to work with adjacency list
                    if colors[w] == -1:
                        continue
                    diff = c - colors[w]

                    if abs(diff) < d:
                        valid = False
                        break
                    elif diff > k_lowest - d:
                        valid = False
                        k_lowest += 1
                        c -= 1      # c will stay unchanged, it increments later
                        break
                    elif -diff > k_lowest - d and c < d:
                        valid = False
                        break
                    elif -diff > k_lowest - d and c >= d:
                        valid = False
                        k_lowest += 1
                        break

                if valid and parent[p] != -1:
                    if c == colors[parent[p]]:
                        valid = False

                if valid:
                    k[d] = max(k_lowest, c + 1)
                    return c

                c += 1

        def dfs_color(v):
            visited[v] = True
            for u in adj[v]:
                if not visited[u]:
                    parent[u] = v
                    colors[u] = find_min_valid_color(u, v)
                    dfs_color(u)

        deg = [len(adj[i]) for i in range(n)] # we make this list to grab the highest degree vertex

        while any(c == -1 for c in colors):
            colored_vertices = [i for i in range(n) if colors[i] == -1]
            v0 = max(colored_vertices, key=lambda i: deg[i])
            colors[v0] = 0
            dfs_color(v0)

        ratio = k[d] / d
        if ratio < chi_c:
            chi_c = ratio
            final_coloring = colors
            best_k = k[d]
            best_d = d

    return best_k, best_d, final_coloring


def main():
    def C(n):
        return [(i, i + 1) for i in range(n - 1)] + [(0, n - 1)]

    triangle_edges = [(0, 1), (0, 2), (1, 2)]
    C5_edges  = C(5)
    C7_edges  = C(7)
    C11_edges = C(11)
    P6_edges  = [(i, i + 1) for i in range(5)]
    two_C5_edges = C(5) + [(i + 5, j + 5) for i, j in C(5)]

    cases = [
        ("Triangle (K3)", 3, 3, triangle_edges, 5),
        ("C5", 5, 5, C5_edges, 5),
        ("C7", 7, 7, C7_edges, 5),
        ("C11", 11, 11, C11_edges, 5),
        ("P6 (path)", 6, 5, P6_edges, 5),
        ("Two disjoint C5s", 10, 10, two_C5_edges, 5),
    ]

    for name, n, m, edges, D in cases:
        best_k, best_d, coloring = approximate_circular_chromatic_number(n, m, edges, D)
        print(f"{name}")
        print(f"The algorithm approximates chi_c as {best_k}/{best_d} = {best_k/best_d:.4f}")
        print(f"The algorithm coloring is: {coloring}\n")


if __name__ == "__main__":
    main()
