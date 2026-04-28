import random


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
    MIN_STEP_SCALE = 0.1  # annealing lower bound for late iterations
    SHIFT_NOISE = 0.05  # small randomness to avoid local optima
    RELAXATION_RETRIES = 20  # temporary high retry count to reduce false negatives

    # if no edges, then chi_c = 1
    if m == 0:
        return 1.0, [0.0] * n

    def initialize_positions(r):
        return [i * r / n for i in range(n)]

    def initialize_random_positions(r):
        return [random.uniform(0.0, r) for _ in range(n)]

    def wrap_delta(delta, r):
        # wrap delta into [-r/2, r/2)
        while delta >= r / 2:
            delta -= r
        while delta < -r / 2:
            delta += r
        return delta

    def relaxation_solver(theta, r):
        theta = theta[:]
        for iteration in range(T):
            cooling = max(MIN_STEP_SCALE, 1.0 - iteration / T)
            shift_sum = [0.0] * n

            for u, v in edges:
                delta = wrap_delta(theta[u] - theta[v], r)
                dist = abs(delta)
                violation = 1.0 - dist

                if violation > 0:
                    shift = (violation / 2.0) * random.uniform(1.0 - SHIFT_NOISE, 1.0 + SHIFT_NOISE)
                    if delta > 0:
                        shift_sum[u] += shift
                        shift_sum[v] -= shift
                    elif delta < 0:
                        shift_sum[u] -= shift
                        shift_sum[v] += shift
                    else:
                        direction = random.choice((-1.0, 1.0))
                        shift_sum[u] += direction * shift
                        shift_sum[v] -= direction * shift

            for v in range(n):
                theta[v] = (theta[v] + ALPHA * cooling * shift_sum[v]) % r

        return theta

    def check_feasible(theta, r):
        for u, v in edges:
            delta = wrap_delta(theta[u] - theta[v], r)
            if abs(delta) < 1.0:
                return False
        return True

    def solve_with_retries(r):
        for attempt in range(RELAXATION_RETRIES):
            if attempt == 0:
                theta = initialize_positions(r)
            else:
                theta = initialize_random_positions(r)

            theta = relaxation_solver(theta, r)

            if check_feasible(theta, r):
                return theta

        return None

    lower = 1.0
    upper = float(n)
    best_angles = initialize_positions(upper)

    for _ in range(B):
        r = (lower + upper) / 2.0
        theta = solve_with_retries(r)

        if theta is not None:
            upper = r
            best_angles = theta
        else:
            lower = r

    return upper, best_angles