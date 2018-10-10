import sys
import inspect
import heapq, random
import cStringIO


class PQ:    #priority queue
    def  __init__(self):
        self.heap = []
        self.count = 0

    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1

    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item

    def isEmpty(self):
        return len(self.heap) == 0

    def update(self, item, priority):
        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

class PQF(PQ):               #priority queue with function
    def  __init__(self, priorityFunction):
        self.priorityFunction = priorityFunction      # store the priority function
        PQ.__init__(self)        # super-class initializer

    def push(self, item):
        PQ.push(self, item, self.priorityFunction(item))

class Hypothesis:          #need to combine this with decoder hypotesis
    def StartHypothesis(self):
        return 0

    def CompletionCheck(self, state):        #whether we have translated all words
        return 0

    def NextProbableHypo(self, state):        #successors of present hypothesis
        return 0

    def HypothesisCombinedCost(self, actions):            #combined cost of hypothesis path till now
        return 0	

hypothes_prob = Hypothesis()               #need to add here		

def UCS(hypothes_prob):
    cost = lambda path: hypothes_prob.HypothesisCombinedCost([x[1] for x in path][1:])
    edge = PQF(cost)
    edge.push([(hypothes_prob.StartHypothesis())])   #push the starting hypothesis here 
    visited = []
    while not edge.isEmpty():
        next_all = edge.pop()
        current = next_all[-1][0]
        if hypothes_prob.CompletionCheck(current):
            return [state[1] for state in next_all][1:]
        if current not in visited:
            visited.append(current)
            for succ in hypothes_prob.NextProbableHypo(current):
                if succ[0] not in visited:
                    Path = next_all[:]
                    Path.append(succ)
                    edge.push(Path)
    return False
	
def aStar(hypothes_prob, heuristic=nullHeuristic):
    cost = lambda path: hypothes_prob.HypothesisCombinedCost([x[1] for x in path][1:]) + heuristic(path[-1][0], hypothes_prob)
    edge = PQF(cost)
    edge.push([(hypothes_prob.StartHypothesis())])
    visited = []
    while not edge.isEmpty():
        next_all = edge.pop()
        current = next_all[-1][0]
        if hypothes_prob.CompletionCheck(current):
            return [state[1] for state in next_all][1:]
        if current not in visited:
            visited.append(current)
            for succ in hypothes_prob.NextProbableHypo(current):
                if succ[0] not in visited:
                    Path = next_all[:]
                    Path.append(succ)
                    edge.push(Path)
    return False