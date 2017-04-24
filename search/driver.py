import string
from collections import deque as q
from Queue import PriorityQueue as pq
from resource import RUSAGE_SELF as r_s
from resource import getrusage as r
from sys import argv
from time import time

o = open('output.txt', 'w')

ib = argv[2]
method = argv[1]
maxdepthlimit = 30

def serializemoves(movelist):


class BoardHist:
    def __init__(self, board, moves=[], inv=False):
        self.board = board
        self.moves = list(moves)
        self.inv = inv

    def extend(self, move):
        newboard = swap(self.board, move)
        newmoves = list(self.moves)
        newmoves.append(move)
        return BoardHist(newboard, moves=newmoves, inv=self.inv)

    def solved(self):
        return self.board == '0,1,2,3,4,5,6,7,8'

    def depth(self):
        return len(self.moves)

    def moveset(self):
        board = self.board
        moves = []
        if self.inv:
            add = lambda x: moves.insert(0, x)
        else:
            add = lambda x: moves.append(x)
        x, y = pos(board)

        if not x == 0:
            add('Up')
        if not x == 2:
            add('Down')
        if not y == 0:
            add('Left')
        if not y == 2:
            add('Right')
        return moves

    def manhattanDist(self):
        # nextBoard = swap(self.board, direction)
        total = 0
        for i in range(0, 8):
            x0 = i / 3
            y0 = i % 3
            x1, y1 = pos(self.board, i)
            total += abs(x0 - x1)
            total += abs(y0 - y1)
        return total

class Frontier:
    def __init__(self, ibh, method='bfs'):
        prevboards = set([ibh.board])

        if method == 'bfs':
            items = q()
            items.appendleft(ibh)
            self.get = items.pop
            self.put = items.appendleft
            self.isEmpty = lambda: len(items) == 0
            self.fsz = lambda: len(items)

        if method == 'dfs' or method == 'ida':
            items = []
            items.append(ibh)
            self.get = items.pop
            self.put = items.append
            self.isEmpty = lambda: len(items) == 0
            self.fsz = lambda: len(items)

        if method == 'ast':
            items = pq()
            items.put((ibh.manhattanDist(), -1, ibh))
            self.get = lambda: items.get()[2]
            self.put = lambda x: items.put((x.manhattanDist(), self.xnd, x))
            self.isEmpty = items.empty
            self.fsz = items.qsize

        self.xtnd = lambda x: prevboards.add(x.board)
        self.contains = lambda x: x in prevboards
        self.maxfsz = 1
        self.maxdepth = 0
        self.xnd = 0

    def populate(self, bh, moves):
        self.xnd += 1
        for mv in moves:
            newbh = bh.extend(mv)
            if not self.contains(newbh.board):
                if self.fsz() == self.maxfsz:
                    self.maxfsz += 1
                if bh.depth() == self.maxdepth:
                    self.maxdepth += 1
                self.put(newbh)
                self.xtnd(newbh)


def swap(board, move):
    l0 = loc(board)
    l = l0
    if move == 'Up':
        l -= 3*2
    elif move == 'Down':
        l += 3*2
    elif move == 'Left':
        l -= 1*2
    elif move == 'Right':
        l += 1*2
    st = board[l]
    trt = string.maketrans('0'+st, st+'0')
    return board.translate(trt)

def pos(board, item=0):
    loc = board.find(str(item)) / 2
    x = loc / 3
    y = loc % 3
    return x, y

def loc(board):
    return board.find('0')

def main(depthlimit = 1):
    t0 = time()
    if method == 'dfs' or method == 'ida':
        inv = True
    else:
        inv = False
    ibh = BoardHist(ib, inv=inv)
    ft = Frontier(ibh, method=method)
    mincost = 100

    while not ft.isEmpty():
        rel = ft.get()
        if method == 'ida' and len(rel.moves) > depthlimit:
            mincost = min(mincost, rel.manhattanDist())
            continue
        if rel.solved():
            t1 = time()
            print >>o, "path_to_goal: %s" % rel.moves
            print >>o, "cost_of_path: %s" % len(rel.moves)
            print >>o, "nodes_expanded: %s" % ft.xnd
            print >>o, "fringe_size: %s" % ft.fsz()
            print >>o, "max_fringe_size: %s" % ft.maxfsz
            print >>o, "search_depth: %s" % rel.depth()
            print >>o, "max_search_depth: %s" % ft.maxdepth
            print >>o, "running_time: %s" % (t1 - t0)
            print >>o, "max_ram_usage: %s" % (r(r_s)[2] / 1024.)
            return True
        moves = rel.moveset()
        ft.populate(rel, moves)
    if method == 'ida' and (depthlimit + mincost) < maxdepthlimit:
        return main(depthlimit + max(mincost, 1))
    print 'ow'
    return False

main()
o.close()
