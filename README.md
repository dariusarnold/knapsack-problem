# 0-1 Knapsack problem

Take a list of items with weight and profit and a maximum weight and determine optimum combination of items that maximizes profit while keeping at or below the weight limit. Every item might only be taken once. The problem is solved using the Nemhauser and Ullmann algorithm.

## Requirements

- Python 3.6+
- no additional libraries required besides the Python standard modules csv and argparse.

## Usage

The program takes its input from a csv file with the following format:
- first line is ignored as input but can be used to comment on the values or the file
- following lines describe one item each
	- every item has a weight and a profit, which are listed in this order and separated by a comma


Call with
```
knapsack.py [-h] FNAME weight_limit
```

## Examples

The repository contains two input files. A small one with 8 items (input1.csv), which was taken from the book "Taschenbuch der Algorithmen - Berthold Vöcking, Helmut Alt,Martin Dietzfelbinger, Rüdiger Reischuk, Christian Scheideler, Heribert Vollmer, Dorothea Wagner) and a larger one with 24 items (input2.csv) from https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html

The expected results are:
File name | Weight limit | Item combination | Optimal profit
-|-|-|-
input1.csv | 643 | 1, 2, 3, 5 | 647
input2.csv | 6404180 | 1, 2, 4, 5, 6, 10, 11, 13, 16, 22, 23, 24 | 13549094


Algorithm output:
```
$ python knapsack.py.py input1.csv 643
Best set: Point(weight=637.0, profit=647.0, items=[1, 2, 3, 5])


$ python knapsack.py.py input2.csv 6404180
Best set: Point(weight=6402560.0, profit=13549094.0, items=[1, 2, 4, 5, 6, 10, 11, 13, 16, 22, 23, 24])
```





