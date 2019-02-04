#!/usr/bin/env python3

import csv
import argparse
import pprint


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
        items = [parse_row(index+1, row) for index, row in enumerate(reader)]
    return items


def merge(old_list, new_list):
    """
    Takes two lists of pareto-optimal points and merges them, discarding points that are dominated by others.
    Point A is dominated by point B if B achieves a larger profit with the same or less weight than A.
    :param old_list: Previous list of pareto optimal points
    :param new_list: New List of pareto optimal points, where one item was added to every point from the old list
    :return: Merged list excluding points that are dominated by others
    """

    def find_larger(list_, value, default=None):
        """
        Return the index of the first item in list__ whose profit is larger than value
        :param list_:
        :param value:
        :return:
        """

        def find(list_, criterion, default):
            """
            Return the index of the first item that satisfies the criterion in list_
            :param list_: Iterable of items to search in
            :param criterion: Function that takes one element and compares true or false
            :return: Index of irst item for which criterion returns true
            """
            return next((index for index, el in enumerate(list_) if criterion(el)), default)

        return find(list_, lambda x: x.profit > value, default)

    merged_list = []
    profit_max = -1
    while True:
        old_pi = find_larger(old_list, profit_max)
        new_pi = find_larger(new_list, profit_max)
        if old_pi is None:
            merged_list += new_list[new_pi:]
            break
        if new_pi is None:
            merged_list += old_list[old_pi:]
            break
        old_p = old_list[old_pi]
        new_p = new_list[new_pi]
        if old_p.weight < new_p.weight or (old_p.weight == new_p.weight and old_p.profit > new_p.profit):
            merged_list.append(old_p)
            profit_max = old_p.profit
        else:
            merged_list.append(new_p)
            profit_max = new_p.profit
    return merged_list


def knapsack(items, weight_limit):
    # create first pareto-optimal list which contains no items
    content = [Point()]
    # add items to possible pareto optimal sets one by one, but merge by only keeping the optimal points
    for item in items:
        content_next = [p + item for p in content]
        content = merge(content, content_next)
    pprint.pprint(content)


def main():
    parser = argparse.ArgumentParser(description="Solve knapsack problem using Nemhauser and Ullmann algorithm.")
    parser.add_argument("csv_filename", metavar="FNAME", help="csv filename containing items weights and values.")
    parser.add_argument("weight_limit", type=float, help="Maximum weight of knapsack in kg")
    args = parser.parse_args()
    items = read_file(args.csv_filename)
    knapsack(items, args.weight_limit)

if __name__ == '__main__':
    main()

