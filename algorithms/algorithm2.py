def circle_relaxation_circular_chromatic_number(n, m, edges, T, B):
    """
    Circle relaxation approximation of the circular chromatic number chi_c(G).

    Parameters
    ----------
    n     : number of vertices (0, 1, ..., n-1)
    m     : number of edges
    edges : list of (i, j) tuples, one entry per edge
    T     : number of relaxation iterations per binary search step
    B     : number of binary search steps

    Returns
    -------
    best_r        : approximated circular chromatic number (float)
    best_angles   : list of length n with the assigned arc starting positions (floats)
    """

    ALPHA = 0.5  # damping factor for force application

    # if no edges, then chi_c = 1
    if m == 0:
        return 1.0, [0.0] * n

    def initialize_positions(r):
        return [i * r / n for i in range(n)]

    def wrap_delta(delta, r):
        # wrap delta into [-r/2, r/2)
        while delta >= r / 2:
            delta -= r
        while delta < -r / 2:
            delta += r
        return delta

    def relaxation_solver(theta, r):
        theta = theta[:]
        for _ in range(T):
            shift_sum = [0.0] * n

            for u, v in edges:
                delta = wrap_delta(theta[u] - theta[v], r)
                dist = abs(delta)
                violation = 1.0 - dist

                if violation > 0:
                    shift = violation / 2.0
                    if delta > 0:
                        shift_sum[u] += shift
                        shift_sum[v] -= shift
                    else:
                        shift_sum[u] -= shift
                        shift_sum[v] += shift

            for v in range(n):
                theta[v] = (theta[v] + ALPHA * shift_sum[v]) % r

        return theta

    def check_feasible(theta, r):
        for u, v in edges:
            delta = wrap_delta(theta[u] - theta[v], r)
            if abs(delta) < 1.0:
                return False
        return True

    lower = 1.0
    upper = float(n)
    best_angles = initialize_positions(upper)

    for _ in range(B):
        r = (lower + upper) / 2.0
        theta = initialize_positions(r)
        theta = relaxation_solver(theta, r)

        if check_feasible(theta, r):
            upper = r
            best_angles = theta
        else:
            lower = r

    return upper, best_angles