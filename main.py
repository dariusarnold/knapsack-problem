#!/usr/bin/env python3

import csv
import argparse


class Item:
    def __init__(self, id, weight, profit):
        """
        :param id: Row of item in csv, int
        """
        self.id = id
        self.weight = weight
        self.profit = profit
        self.ratio = profit/weight

    def __repr__(self):
        return f"Item(id={self.id}, weight={self.weight}, profit={self.profit})"


def read_file(filename):
    """
    Read file and return list of items
    :param filename: csv input filename
    """

    def parse_row(index, row):
        """
        :param row: row is a list of two strings, first the weight, then the price
        :return: Item instance for the given row
        """
        weight, price = (float(number) for number in row)
        return Item(index, weight, price)

    with open(filename, "r") as f:
        reader = csv.reader(f)
        # skip header, read item rows
        next(reader)
        items = [parse_row(index, row) for index, row in enumerate(reader)]
    return items


def knapsack(filename):
    print(read_file(filename))
    # create first pareto-optimal list which contains no items
    content = []


def main():
    parser = argparse.ArgumentParser(description="Solve knapsack problem using Nemhauser and Ullmann algorithm.")
    parser.add_argument("csv_filename", metavar="FNAME", help="csv filename containing items weights and values.")
    args = parser.parse_args()
    knapsack(args.csv_filename)

if __name__ == '__main__':
    main()

