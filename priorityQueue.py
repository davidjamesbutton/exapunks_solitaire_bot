import heapq

class MinPriorityQueue:
    def __init__(self):
        self.queue = []

    def __len__(self):
        return len(self.queue)

    def enqueue(self, comparable):
        heapq.heappush(self.queue, comparable)

    def dequeue(self):
        return heapq.heappop(self.queue)

class MaxPriorityQueue:
    def __init__(self, ):
        self.minPriorityQueue = MinPriorityQueue()

    def __len__(self):
        return len(self.minPriorityQueue)

    def enqueue(self, comparable):
        self.minPriorityQueue.enqueue(ReversedComparable(comparable))

    def dequeue(self):
        reversed_comparable = self.minPriorityQueue.dequeue()
        return reversed_comparable.comparable

class ReversedComparable:
    def __init__(self, comparable):
        self.comparable = comparable

    def __lt__(self, other):
        return other.comparable < self.comparable