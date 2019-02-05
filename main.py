#!/usr/bin/env python3

import csv
import argparse


class Item:
    def __init__(self, id, weight, profit):
        """
        Represent one item that can be put into the knapsack.
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


def find(list_, criterion, default):
    """
    Return the index of the first item that satisfies the criterion in list_. If no item satisfies the criterion,
    the default value is returned
    :param list_: Iterable of items to search in
    :param criterion: Function that takes one element and compares true or false
    :param default: Default value to return if no item matches criterion
    :return: Index of first item for which criterion returns true
    """
    return next((index for index, el in enumerate(list_) if criterion(el)), default)


def find_larger_profit(list_, value, default=None):
    """
    Return the index of the first item in list__ whose profit is larger than value
    """
    return find(list_, lambda x: x.profit > value, default)


def find_max_below(list_, value, default=None):
    """
    Return the index of the item in the list whose weight is closest to, but smaller than value
    """
    return find(list_, lambda x: x.weight > value, default) - 1


def merge(old_list, new_list, weight_limit):
    """
    Takes two lists of pareto-optimal points and merges them, discarding points that are dominated by others.
    Point A is dominated by point B if B achieves a larger profit with the same or less weight than A.
    :param old_list: Previous list of pareto optimal points
    :param new_list: New List of pareto optimal points, where one item was added to every point from the old list
    :param weight_limit: Max weight to reduce number of points
    :return: Merged list excluding points that are dominated by others
    """

    merged_list = []
    profit_max = -1
    while True:
        old_point_index = find_larger_profit(old_list, profit_max)
        new_point_index = find_larger_profit(new_list, profit_max)
        # merge other list if one doesn't contain a point with profit above the current limit
        # or the found point is above the weight limit
        if old_point_index is None or old_list[old_point_index].weight > weight_limit:
            merged_list += new_list[new_point_index:]
            break
        if new_point_index is None or new_list[new_point_index].weight > weight_limit:
            merged_list += old_list[old_point_index:]
            break
        old_p = old_list[old_point_index]
        new_p = new_list[new_point_index]
        if old_p.weight < new_p.weight or (old_p.weight == new_p.weight and old_p.profit > new_p.profit):
            merged_list.append(old_p)
            profit_max = old_p.profit
        else:
            merged_list.append(new_p)
            profit_max = new_p.profit
    return merged_list


def knapsack(items, weight_limit):
    """
    Solve 01-knapsack problem for given list of items and weight limit.
    :param items: list of possible items to chose from. No multiples of one item will be taken.
    :param weight_limit: Maximim weight to fill knapsack to
    :return: Ids of items in the list of items, starting at 1 for the first item in the list
    """
    # create first pareto-optimal list which contains no items
    content = [Point()]
    # add items to possible pareto optimal sets one by one, but merge by only keeping the optimal points
    for item in items:
        # filter out item combinations that lie above the weight limit
        content_next = [point + item for point in content]
        content = merge(content, content_next, weight_limit)
    best_combination_below_limit = content[find_max_below(content, weight_limit)]
    print(f"Best set: {best_combination_below_limit}")
    return best_combination_below_limit.item_ids


def main():
    parser = argparse.ArgumentParser(description="Solve knapsack problem using Nemhauser and Ullmann algorithm.")
    parser.add_argument("csv_filename", metavar="FNAME", help="csv filename containing items weights and values.")
    parser.add_argument("weight_limit", type=float, help="Maximum weight of knapsack in kg")
    args = parser.parse_args()
    items = read_file(args.csv_filename)
    knapsack(items, args.weight_limit)


if __name__ == '__main__':
    main()
