from collections import defaultdict

import copy


class DependencyHelper(object):
    def __init__(self):
        self.graph = defaultdict(set)

    def add(self, a, b):
        self.graph[a].add(b)
        return None

    def remove(self, a, b):
        if b in self.graph[a]:
            self.graph[a].remove(b)
        return None

    def get_dependent(self, item):
        return list(self.graph[item])

    def has_dependencies(self):
        path = set()

        def dfs(u):
            path.add(u)
            for v in self.graph.get(u):
                if v in path or dfs(v):
                    return True
            path.remove(u)
            return False

        return any(dfs(v) for v in self.graph)

    def copy(self):
        return copy.deepcopy(self)

    def __add__(self, (a, b)):
        helper = self.copy()
        helper.add(a, b)
        return helper

    def __sub__(self, (a, b)):
        helper = self.copy()
        helper.remove(a, b)
        return helper

    def __nonzero__(self):
        return not self.has_dependencies()
