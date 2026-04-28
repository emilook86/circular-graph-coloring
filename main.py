import argparse
import sys
import math

from algorithms.algorithm1 import approximate_circular_chromatic_number as alg1_func
from algorithms.algorithm3 import greedy_bfs_circular_chromatic_number as alg3_func


def parse_args():
    parser = argparse.ArgumentParser(
        description="Circular Graph Coloring - Approximation Algorithms"
    )
    parser.add_argument(
        "-a", "--algorithm",
        type=int,
        choices=[1, 2, 3],
        required=True,
        help="Algorithm to use: 1 (DFS-based), 2 (Circle relaxation), 3 (Greedy-BFS)"
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        required=True,
        help="Input file path"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Output file path (default: stdout)"
    )
    return parser.parse_args()


def read_input_file(filepath):
    with open(filepath, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


def write_output_file(filepath, content):
    with open(filepath, 'w') as f:
        f.write(content)


def run_algorithm1(edges, n, m, D):
    best_k, best_d, coloring = alg1_func(n, m, edges, D)
    ratio = best_k / best_d
    output = []
    output.append(f"Approximation of chi_c: {best_k}/{best_d} = {ratio:.4f}")
    output.append(f"Coloring: {' '.join(map(str, coloring))}")
    return "\n".join(output) + "\n"


def run_algorithm2(edges, n, m, T, B):
    return "Algorithm 2 (Circle relaxation) is not yet implemented.\n"


def run_algorithm3(edges, n, m, K):
    best_k, best_d, coloring = alg3_func(n, m, edges, K)
    ratio = best_k / best_d
    output = []
    output.append(f"Approximation of chi_c: {best_k}/{best_d} = {ratio:.4f}")
    output.append(f"Coloring: {' '.join(map(str, coloring))}")
    return "\n".join(output) + "\n"


def main():
    args = parse_args()

    lines = read_input_file(args.input)

    if args.algorithm == 1:
        n, m = map(int, lines[0].split())
        edges = []
        for i in range(1, m + 1):
            u, v = map(int, lines[i].split())
            edges.append((u, v))
        D = int(lines[m + 1])
        output = run_algorithm1(edges, n, m, D)

    elif args.algorithm == 2:
        n, m = map(int, lines[0].split())
        edges = []
        for i in range(1, m + 1):
            u, v = map(int, lines[i].split())
            edges.append((u, v))
        T, B = map(int, lines[m + 1].split())
        output = run_algorithm2(edges, n, m, T, B)

    elif args.algorithm == 3:
        n, m = map(int, lines[0].split())
        edges = []
        for i in range(1, m + 1):
            u, v = map(int, lines[i].split())
            edges.append((u, v))
        K = int(lines[m + 1])
        output = run_algorithm3(edges, n, m, K)

    if args.output:
        write_output_file(args.output, output)
    else:
        print(output, end="")


if __name__ == "__main__":
    main()