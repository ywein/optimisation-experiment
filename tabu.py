"""
This is pure Python implementation of Tabu search algorithm for a Travelling Salesman Problem, that the distances
between the cities are symmetric (the distance between city 'a' and city 'b' is the same between city 'b' and city 'a').
The TSP can be represented into a graph. The cities are represented by nodes and the distance between them is
represented by the weight of the ark between the nodes.

The .txt file with the graph has the form:

node1 node2 distance_between_node1_and_node2
node1 node3 distance_between_node1_and_node3
...

Be careful node1, node2 and the distance between them, must exist only once. This means in the .txt file
should not exist:
node1 node2 distance_between_node1_and_node2
node2 node1 distance_between_node2_and_node1

For pytests run following command:
pytest

For manual testing run:
python tabu_search.py -f your_file_name.txt -number_of_iterations_of_tabu_search -s size_of_tabu_search
e.g. python tabu_search.py -f tabudata2.txt -i 4 -s 3
"""

import copy
import argparse

from local import generateRandomSolution, localSearchOneStep



# def generate_neighbours(path):
#     """
#     Pure implementation of generating a dictionary of neighbors and the cost with each
#     neighbor, given a path file that includes a graph.
#
#     :param path: The path to the .txt file that includes the graph (e.g.tabudata2.txt)
#     :return dict_of_neighbours: Dictionary with key each node and value a list of lists with the neighbors of the node
#     and the cost (distance) for each neighbor.
#
#     Example of dict_of_neighbours:
#     >>) dict_of_neighbours[a]
#     [[b,20],[c,18],[d,22],[e,26]]
#
#     This indicates the neighbors of node (city) 'a', which has neighbor the node 'b' with distance 20,
#     the node 'c' with distance 18, the node 'd' with distance 22 and the node 'e' with distance 26.
#
#     """
#
#     dict_of_neighbours = {}
#
#     with open(path) as f:
#         for line in f:
#             if line.split()[0] not in dict_of_neighbours:
#                 _list = list()
#                 _list.append([line.split()[1], line.split()[2]])
#                 dict_of_neighbours[line.split()[0]] = _list
#             else:
#                 dict_of_neighbours[line.split()[0]].append(
#                     [line.split()[1], line.split()[2]]
#                 )
#             if line.split()[1] not in dict_of_neighbours:
#                 _list = list()
#                 _list.append([line.split()[0], line.split()[2]])
#                 dict_of_neighbours[line.split()[1]] = _list
#             else:
#                 dict_of_neighbours[line.split()[1]].append(
#                     [line.split()[0], line.split()[2]]
#                 )
#
#     return dict_of_neighbours


# def generate_first_solution(path, dict_of_neighbours):
#     """
#     Pure implementation of generating the first solution for the Tabu search to start, with the redundant resolution
#     strategy. That means that we start from the starting node (e.g. node 'a'), then we go to the city nearest (lowest
#     distance) to this node (let's assume is node 'c'), then we go to the nearest city of the node 'c', etc
#     till we have visited all cities and return to the starting node.
#
#     :param path: The path to the .txt file that includes the graph (e.g.tabudata2.txt)
#     :param dict_of_neighbours: Dictionary with key each node and value a list of lists with the neighbors of the node
#     and the cost (distance) for each neighbor.
#     :return first_solution: The solution for the first iteration of Tabu search using the redundant resolution strategy
#     in a list.
#     :return distance_of_first_solution: The total distance that Travelling Salesman will travel, if he follows the path
#     in first_solution.
#
#     """
#
#     with open(path) as f:
#         start_node = f.read(1)
#     end_node = start_node
#
#     first_solution = []
#
#     visiting = start_node
#
#     distance_of_first_solution = 0
#     while visiting not in first_solution:
#         minim = 10000
#         for k in dict_of_neighbours[visiting]:
#             if int(k[1]) < int(minim) and k[0] not in first_solution:
#                 minim = k[1]
#                 best_node = k[0]
#
#         first_solution.append(visiting)
#         distance_of_first_solution = distance_of_first_solution + int(minim)
#         visiting = best_node
#
#     first_solution.append(end_node)
#
#     position = 0
#     for k in dict_of_neighbours[first_solution[-2]]:
#         if k[0] == start_node:
#             break
#         position += 1
#
#     distance_of_first_solution = (
#         distance_of_first_solution
#         + int(dict_of_neighbours[first_solution[-2]][position][1])
#         - 10000
#     )
#     return first_solution, distance_of_first_solution


# def find_neighborhood(solution, dict_of_neighbours):
#     """
#     Pure implementation of generating the neighborhood (sorted by total distance of each solution from
#     lowest to highest) of a solution with 1-1 exchange method, that means we exchange each node in a solution with each
#     other node and generating a number of solution named neighborhood.
#
#     :param solution: The solution in which we want to find the neighborhood.
#     :param dict_of_neighbours: Dictionary with key each node and value a list of lists with the neighbors of the node
#     and the cost (distance) for each neighbor.
#     :return neighborhood_of_solution: A list that includes the solutions and the total distance of each solution
#     (in form of list) that are produced with 1-1 exchange from the solution that the method took as an input
#
#
#     Example:
#     >>) find_neighborhood(['a','c','b','d','e','a'])
#     [['a','e','b','d','c','a',90], [['a','c','d','b','e','a',90],['a','d','b','c','e','a',93],
#     ['a','c','b','e','d','a',102], ['a','c','e','d','b','a',113], ['a','b','c','d','e','a',93]]
#
#     """
#
#     neighborhood_of_solution = []
#
#     for n in solution[1:-1]:
#         idx1 = solution.index(n)
#         for kn in solution[1:-1]:
#             idx2 = solution.index(kn)
#             if n == kn:
#                 continue
#
#             _tmp = copy.deepcopy(solution)
#             _tmp[idx1] = kn
#             _tmp[idx2] = n
#
#             distance = 0
#
#             for k in _tmp[:-1]:
#                 next_node = _tmp[_tmp.index(k) + 1]
#                 for i in dict_of_neighbours[k]:
#                     if i[0] == next_node:
#                         distance = distance + int(i[1])
#             _tmp.append(distance)
#
#             if _tmp not in neighborhood_of_solution:
#                 neighborhood_of_solution.append(_tmp)
#
#     indexOfLastItemInTheList = len(neighborhood_of_solution[0]) - 1
#
#     neighborhood_of_solution.sort(key=lambda x: x[indexOfLastItemInTheList])
#     return neighborhood_of_solution


def tabu_search(
    first_solution, iters, size, find_neighborhood, evaluate
):
    """
    Pure implementation of Tabu search algorithm for a Travelling Salesman Problem in Python.

    :param first_solution: The solution for the first iteration of Tabu search using the redundant resolution strategy
    in a list.
    :param distance_of_first_solution: The total distance that Travelling Salesman will travel, if he follows the path
    in first_solution.
    :param dict_of_neighbours: Dictionary with key each node and value a list of lists with the neighbors of the node
    and the cost (distance) for each neighbor.
    :param iters: The number of iterations that Tabu search will execute.
    :param size: The size of Tabu List.
    :return best_solution_ever: The solution with the lowest distance that occurred during the execution of Tabu search.
    :return best_cost: The total distance that Travelling Salesman will travel, if he follows the path in best_solution
    ever.

    """
    count = 1
    solution = first_solution
    best_cost = evaluate(first_solution)
    best_solution_ever = solution

    tabuList = []

    while count <= iters and best_cost != 0:
        # get all of the neighbors
        neighbors = find_neighborhood(solution)

        # find all neighbors that are not part of the Tabu list
        neighbors = list(filter(lambda n: n not in tabuList, neighbors))
        # pick the best neighbor solution
        if len(neighbors) > 0:
            evaluated = sorted(neighbors, key=lambda n: evaluate(n))
            solution = evaluated[0]
            # get the cost between the two solutions
            cost = evaluate(best_solution_ever) - evaluate(solution)
            # if the new solution is better,
            # update the current solution with the new solution
            if cost >= 0:
                best_solution_ever = solution

            # add new solution to the Tabu list
            tabuList.append(solution)

            if len(tabuList) > size:
                tabuList.pop(0)

        count += 1

    print("iter num", count)

    return best_solution_ever, best_cost
