# AUTOGENERATED! DO NOT EDIT! File to edit: 05_Prim_spanning_tree.ipynb (unless otherwise specified).

__all__ = ['Row', 'spanning_tree']

# Cell
from queue import Queue
from typing import List, Dict
from collections import namedtuple

import graph_utils.core as gu
from .dijsktra import priority_dict

# Cell
Row = namedtuple('Node', ['distance_from_source', 'preceding_vertex'])

# Cell
def spanning_tree(graph:gu.Graph, source):
    distance_table = dict()

    # initiate an empty distance table
    for i in range(graph.numVertices):
        #distance_table[i] = Row(distance_from_source=None, preceding_vertex=None)
        distance_table[i] = Row(None, None)

    # distance to the source from itself is 0
    distance_table[source] = Row(0, source)

    # Holds mapping of vertex id to distance
    # from source. Access the highest priority (lowest distance)
    # item first
    priority_queue = priority_dict()
    # priority_queue[vertex number] = distance

    priority_queue[source] = 0

    visited_vertices = set()

    # Set of edges where each edge represented as a string
    # "1->2 is an edge between vertices 1 and 2"
    spanning_tree = set()

    while priority_queue:

        current_vertex = priority_queue.pop_smallest()

        if current_vertex in visited_vertices:
            continue

        visited_vertices.add(current_vertex)

        if current_vertex != source:
            last_vertex = distance_table[current_vertex][1]

            edge = f"{last_vertex}->{current_vertex}"

            if edge not in spanning_tree:
                spanning_tree.add(edge)

        for neighbor in graph.get_adjacent_vertices(current_vertex):

            distance = g.get_edge_weight(current_vertex, neighbor)

            neighbor_distance = distance_table[neighbor][0]

            if neighbor_distance is None or neighbor_distance > distance:
                distance_table[neighbor] = Row(distance, current_vertex)
                priority_queue[neighbor] = distance




    return spanning_tree