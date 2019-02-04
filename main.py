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


class Point:
    def __init__(self, weight=0., profit=0.):
        """
        Represent a point in the weight/profit diagram. A point is created by a combination of items.
        The IDs of the items used to create this point is saved in item_ids
        :param weight: Sum of the weights of all items in this set
        :param profit: Sum of the profits of all items in this set
        """
        self.weight = weight
        self.profit = profit
        self.item_ids = []

    def __add__(self, item):
        """
        Add an item to this point by adding its weight and profit to the weight and profit
        of the point and also saving its id.
        :param item:
        :return:
        """
        moved_point = Point(self.weight+item.weight, self.profit+item.profit)
        moved_point.item_ids = self.item_ids.copy()
        moved_point.item_ids.append(item.id)
        return moved_point

    def __repr__(self):
        return f"Point(weight={self.weight}, profit={self.profit}, items={self.item_ids})"


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
    parser.add_argument("weight_limit", type=float, help="Maximum weight of knapsack in kg")
    args = parser.parse_args()
    knapsack(args.csv_filename)

if __name__ == '__main__':
    main()

