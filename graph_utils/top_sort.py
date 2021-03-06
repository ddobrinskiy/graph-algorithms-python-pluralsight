# AUTOGENERATED! DO NOT EDIT! File to edit: 02_topological_sort.ipynb (unless otherwise specified).

__all__ = ['topological_sort']

# Cell
from queue import Queue
from typing import List

import graph_utils.core as gu
import graph_utils.traversal as gut

# Cell
def topological_sort(graph:gu.Graph) -> List:
    """calc topological sort of a DAG"""

    queue = Queue()

    indegreeMap = dict()

    for i in range(graph.numVertices):
        indegreeMap[i] = graph.get_indegree(i)

        # Queue all nodes with no dependencies, i.e. no edges coming in
        if indegreeMap[i] == 0:
            queue.put(i)

        sortedList = []

    while not queue.empty():

        vertex = queue.get()

        sortedList.append(vertex)

        for v in graph.get_adjacent_vertices(vertex):

            # decrement by one
            indegreeMap[v] -= 1

            if indegreeMap[v] == 0:
                queue.put(v)

    if len(sortedList) != graph.numVertices:
        raise ValueError("This graph has a cycle!")


    return sortedList


