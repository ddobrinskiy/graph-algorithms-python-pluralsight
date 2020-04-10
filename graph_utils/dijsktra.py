# AUTOGENERATED! DO NOT EDIT! File to edit: 04_dijsktra.ipynb (unless otherwise specified).

__all__ = ['priority_dict', 'Row', 'build_distance_table']

# Cell
from queue import Queue
from typing import List, Dict
from collections import namedtuple

import pandas as pd

import graph_utils.core as gu
from .shortest_path import shortest_path

# Cell

# https://code.activestate.com/recipes/522995-priority-dict-a-priority-queue-with-updatable-prio/

from heapq import heapify, heappush, heappop

class priority_dict(dict):
    """Dictionary that can be used as a priority queue.

    Keys of the dictionary are items to be put into the queue, and values
    are their respective priorities. All dictionary methods work as expected.
    The advantage over a standard heapq-based priority queue is
    that priorities of items can be efficiently updated (amortized O(1))
    using code as 'thedict[item] = new_priority.'

    The 'smallest' method can be used to return the object with lowest
    priority, and 'pop_smallest' also removes it.

    The 'sorted_iter' method provides a destructive sorted iterator.
    """

    def __init__(self, *args, **kwargs):
        super(priority_dict, self).__init__(*args, **kwargs)
        self._rebuild_heap()

    def _rebuild_heap(self):
        self._heap = [(v, k) for k, v in self.items()]
        heapify(self._heap)

    def smallest(self):
        """Return the item with the lowest priority.

        Raises IndexError if the object is empty.
        """

        heap = self._heap
        v, k = heap[0]
        while k not in self or self[k] != v:
            heappop(heap)
            v, k = heap[0]
        return k

    def pop_smallest(self):
        """Return the item with the lowest priority and remove it.

        Raises IndexError if the object is empty.
        """

        heap = self._heap
        v, k = heappop(heap)
        while k not in self or self[k] != v:
            v, k = heappop(heap)
        del self[k]
        return k

    def __setitem__(self, key, val):
        # We are not going to remove the previous value from the heap,
        # since this would have a cost O(n).

        super(priority_dict, self).__setitem__(key, val)

        if len(self._heap) < 2 * len(self):
            heappush(self._heap, (val, key))
        else:
            # When the heap grows larger than 2 * len(self), we rebuild it
            # from scratch to avoid wasting too much memory.
            self._rebuild_heap()

    def setdefault(self, key, val):
        if key not in self:
            self[key] = val
            return val
        return self[key]

    def update(self, *args, **kwargs):
        # Reimplementing dict.update is tricky -- see e.g.
        # http://mail.python.org/pipermail/python-ideas/2007-May/000744.html
        # We just rebuild the heap from scratch after passing to super.

        super(priority_dict, self).update(*args, **kwargs)
        self._rebuild_heap()

    def sorted_iter(self):
        """Sorted iterator of the priority dictionary items.

        Beware: this will destroy elements as they are returned.
        """

        while self:
            yield self.pop_smallest()


# Cell
Row = namedtuple('Node', ['distance_from_source', 'preceding_vertex'])

# Cell
def build_distance_table(graph:gu.Graph, source:int):
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

    while priority_queue:
        current_vertex = priority_queue.pop_smallest()

        current_distance = distance_table[current_vertex][0]

        for neigbor in graph.get_adjacent_vertices(current_vertex):
            distance = current_distance + g.get_edge_weight(current_vertex, neigbor)

            neigbor_distance = distance_table[neigbor][0]

            if neigbor_distance is None or neigbor_distance > distance:
                distance_table[neigbor] = Row(distance, current_vertex)

                priority_queue[neigbor] = distance


    return distance_table