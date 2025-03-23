# Time-Based Storage Examples

This directory contains example scripts demonstrating how to use the Time-Based Storage package.

## Available Examples

### 1. RB-Tree Basic Example (`rbtree_example.py`)

A simple example showing basic usage of the Red-Black Tree implementation for time-based storage.

Run with:
```bash
python rbtree_example.py
```

This example demonstrates:
- Basic operations with the RB-Tree implementation
- Thread-safe usage of the RB-Tree implementation
- Timestamp collision handling

### 2. RB-Tree Performance Benchmark (`rbtree_benchmark.py`)

A comprehensive benchmark comparing the performance of the standard implementation with the Red-Black Tree implementation.

Run with:
```bash
# Default run with 100K elements
python rbtree_benchmark.py

# Run with a custom number of elements (e.g., 500K)
python rbtree_benchmark.py 500000
```

This benchmark measures and compares:
- Insertion performance for random and sorted timestamps
- Range query performance for different range sizes
- Performance speedup ratios for each operation

## More Examples

For more comprehensive examples, see the `docs/examples.py` file in the project's documentation directory. This contains examples for all storage implementations, including:

- Basic usage
- Timestamp collision handling
- Thread-safe operations
- Performance comparisons
- Real-world use cases (event monitoring system)

## Project-wide Benchmarks

The project also includes a comprehensive benchmark script at the root level (`benchmark.py`) which compares all three implementations (Standard, Heap, and RB-Tree) across various operations and dataset sizes. 