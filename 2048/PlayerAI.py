from BaseAI import BaseAI
import time

class PlayerAI(BaseAI):
    def getMove(self, grid):
        moves = grid.getAvailableMoves()
        self.t0 = time.clock()
        # HEURISTIC: Max tile, remaining cells

        high = -float('inf')
        mv = 0

        for move in moves:
            gridc = grid.clone()
            gridc.move(move)
            a = self.minimax(gridc, high, 1)
            if a > high:
                high = a
                mv = move

        print time.clock() - self.t0
        return mv

        for move in moves:
            gd1 = grid.clone()
            gd1.move(move)
            insercells = gd1.getAvailableCells()
            low = float('inf')
            for cell in insercells:
                gdo1 = gd1.clone()
                gdo1.insertTile(cell, 2)
                moves2 = gdo1.getAvailableMoves()
                hi = -float('inf')
                for move2 in moves2:
                    gd2 = gdo1.clone()
                    gd2.move(move2)
                    ic2 = gd2.getAvailableCells()
                    lo = float('inf')
                    for c2 in ic2:
                        gdo2 = gd2.clone()
                        gdo2.insertTile(c2, 2)
                        moves3 = gdo2.getAvailableMoves()
                        h = -float('inf')
                        for move3 in moves3:
                            gd3 = gdo2.clone()
                            gd3.move(move3)
                            count = sum(item*item for sublist in gd3.map for item in sublist)
                            if count > h:
                                h = count
                        if h < lo:
                            lo = h
                    if lo > hi:
                        hi = count
                if hi < low:
                    low = hi
            if low > high:
                high = low
                mv = move

        return mv

    def minimax(self, grid, alpha, depth=0):
        """
        Calculates heuristic score of the grid at future points
        """
        if depth == 0:    # or time.clock() - 0.1 > 0:
            return sum(item*item for sublist in grid.map for item in sublist)

        mini = float('inf')
        cells = grid.getAvailableCells()
        for cell, num in [(cell, num) for cell in cells for num in [2, 4]]:
            gridcopy = grid.clone()
            gridcopy.insertTile(cell, num)
            moves = gridcopy.getAvailableMoves()
            maxi = -float('inf')
            for move in moves:
                gc = grid.clone()
                gc.move(move)
                beta = self.minimax(gc, alpha, depth-1)
                if beta < alpha:
                    break
                if beta > maxi:
                    maxi = beta
            if maxi < mini:
                mini = maxi
                if mini > alpha:
                    alpha = mini
        return alpha
