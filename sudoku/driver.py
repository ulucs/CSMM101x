import sys

if __name__ == '__main__':

    domain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    sqLetter = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
    sqNumber = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
    squares = [[l + n for l in sqLetterSS for n in sqNumberSS] for sqLetterSS in sqLetter for sqNumberSS in sqNumber]
    lines = [[l + n for sqNumberSS in sqNumber for n in sqNumberSS] for sqLetterSS in sqLetter for l in sqLetterSS]
    columns = [[l + n for sqLetterSS in sqLetter for l in sqLetterSS] for sqNumberSS in sqNumber for n in sqNumberSS]
    boardEls = [l + n for sqLetterSS in sqLetter for l in sqLetterSS for sqNumberSS in sqNumber for n in sqNumberSS]

    constraints = [lines, columns, squares]

    def printboard(brd):
        for line in lines:
            print [brd[i] for i in line]

    def board2string(brd):
        return ''.join((str(brd[t]) if type(brd[t]) is int else '0' for t in boardEls))

    def string2board(eb):
        brd = {}
        for idx, num in enumerate(eb):
            target = boardEls[idx]
            if num != '0':
                brd[target] = int(num)
            else:
                brd[target] = domain.copy()
        return brd

    def getassigned(brd, sqnames):
        return {brd[t] for t in sqnames if type(brd[t]) is int}

    def getunassignednames(brd, sqnames):
        return [t for t in sqnames if type(brd[t]) is set]

    def applyconstraints(brd):
        for conssuperset in constraints:
            for consset in conssuperset:
                setcons = getassigned(brd, consset)
                for consel in getunassignednames(brd, consset):
                    brd[consel] -= setcons
        return brd

    def issolved(eb):
        return '0' not in eb

    def isfailure(brd):
        return any([len(brd[t]) == 0 for t in boardEls if type(brd[t]) is set])

    def backtrack(bstr):
        if issolved(bstr):
            return bstr

        sboard = string2board(bstr)
        sboard = applyconstraints(sboard)
        if isfailure(sboard):
            return False

        btspot = getunassignednames(sboard, boardEls)[0]
        btvals = sboard[btspot]
        for val in btvals:
            sboard[btspot] = val
            res = backtrack(board2string(sboard))
            if type(res) is str:
                return res
        return False

    solution = backtrack(sys.argv[1])
    with open('output.txt', 'w') as f:
        f.write(solution)
