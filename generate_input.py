import argparse
import random


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate random graph input files for circular coloring"
    )
    parser.add_argument(
        "-a", "--algorithm",
        type=int,
        choices=[1, 2, 3],
        required=True,
        help="Algorithm: 1, 2, or 3"
    )
    parser.add_argument(
        "-n", "--vertices",
        type=int,
        default=10,
        help="Number of vertices (default: 10)"
    )
    parser.add_argument(
        "-e", "--edges",
        type=int,
        default=None,
        help="Number of edges (if -p not set, this is exact count)"
    )
    parser.add_argument(
        "-p", "--probability",
        type=float,
        default=None,
        help="Edge probability for G(n,p) model (0.0-1.0)"
    )
    parser.add_argument(
        "--param",
        type=str,
        default=None,
        help="Parameter: D (alg1), T B (alg2), K (alg3). Auto if not set."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        required=True,
        help="Output file path"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility"
    )
    return parser.parse_args()


def generate_random_graph(n, edge_count=None, probability=None, seed=None):
    if seed is not None:
        random.seed(seed)

    edges = set()
    
    if probability is not None:
        max_edges = n * (n - 1) // 2
        target_edges = int(max_edges * probability)
    elif edge_count is not None:
        target_edges = edge_count
    else:
        target_edges = n * 2

    max_edges = n * (n - 1) // 2
    target_edges = min(target_edges, max_edges)

    while len(edges) < target_edges:
        u = random.randint(0, n - 1)
        v = random.randint(0, n - 1)
        if u < v:
            edges.add((u, v))
        elif v < u:
            edges.add((v, u))

    m = len(edges)
    return n, m, list(edges)


def write_input_file(filepath, n, m, edges, algorithm, param):
    with open(filepath, 'w') as f:
        f.write(f"{n} {m}\n")
        for u, v in edges:
            f.write(f"{u} {v}\n")
        if algorithm == 2:
            T, B = param.split()
            f.write(f"{T} {B}\n")
        else:
            f.write(f"{param}\n")


def main():
    args = parse_args()

    if args.seed is not None:
        random.seed(args.seed)

    default_params = {
        1: args.vertices,
        2: (40, 500),
        3: args.vertices
    }

    param = args.param
    if param is None:
        if args.algorithm == 2:
            param = f"{default_params[2][0]} {default_params[2][1]}"
        else:
            param = str(default_params[args.algorithm])

    for i in range(1):
        n, m, edges = generate_random_graph(
            args.vertices,
            args.edges,
            args.probability
        )

        write_input_file(args.output, n, m, edges, args.algorithm, param)
        print(f"Generated: {args.output} (n={n}, m={m})")


if __name__ == "__main__":
    main()