# Circular Graph Coloring

Approximation algorithms for circular chromatic number.

## Generate Input
```bash
python3 generate_input.py -a ALG -n N -e E [-p PROB] -o FILE
```

| Flag | Description | Default |
|------|-------------|---------|
| -a | Algorithm (1, 2, 3) | required |
| -n | Number of vertices | 10 |
| -e | Number of edges | 2×n |
| -p | Edge probability 0.0-1.0 | - |
| --param | Override param (D/K/T B) | auto |
| --seed | Random seed | - |
| -o | Output file | required |

Auto params: alg1 → D=n, alg2 → "40 500", alg3 → K=n

## Run Algorithm
```bash
python3 main.py -a ALG -i FILE [-o FILE]
```

| Flag | Description |
|------|-------------|
| -a | Algorithm (1, 2, 3) |
| -i | Input file |
| -o | Output file (stdout if omitted) |

## Input Format
```
n m
u v
...
u v
D          (alg1)
# or
T B        (alg2)
# or
K          (alg3)
```

## Output Format
```
Approximation of chi_c: k/d = ratio
Coloring: c0 c1 c2 ...
```

## Examples
```bash
# Generate and run
python3 generate_input.py -a 1 -n 20 -e 30 -o inputs/alg1/g.txt
python3 main.py -a 1 -i inputs/alg1/g.txt

# Custom param
python3 generate_input.py -a 1 -n 20 --param 10 -o inputs/alg1/g.txt
```