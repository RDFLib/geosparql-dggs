from itertools import product

zero_cells = ["N", "O", "P", "Q", "R", "S"]
N_crs = {'auspix': 3}


class CellCollection:
    """
    DGGS Cell Collection class.
    A collection of Cell instances
    ***NB cells are handled as being un-ordered in this implementation.***

    """

    def __init__(self, cells):
        """
        :param cells: a list of Cell objects
        """
        self.cells = cells
        self.validate()
        self.crs = self.cells[0].crs
        self.kind = self.cells[0].kind
        self.cell_suids = [cell.suid for cell in self.cells]
        self.compress()
        self.deduplicate()
        self.absorb()
        self.order()

    def __repr__(self):
        return ' '.join(self.cell_suids)

    def validate(self):
        # input can be a list of strings
        # all cells must have the same CRS
        if isinstance(self.cells, str):
            self.cells = [Cell(self.cells)]
        if isinstance(self.cells, Cell):
            self.cells = [self.cells]
        # at this point single instances have been coerced to a list with a Cell
        # convert lists of strings to lists of Cells
        assert isinstance(self.cells, list)
        if isinstance(self.cells[0], str):
            self.cells = [Cell(cell_str) for cell_str in self.cells]
        # finally check we have a list of Cell objects with consistent CRSs
        for cell in self.cells:
            assert isinstance(cell, Cell)

    def deduplicate(self):
        # remove repeated instances of the same cell
        self.cell_suids = list(set(self.cell_suids))

    def absorb(self):
        # absorb child cells in to parent cells (where the parent cell exists)
        # e.g. P1 P12 is equivalent to P1, so remove P12 if present
        for suid in self.cell_suids:
            for i in range(len(suid)-1):
                ancestor = suid[0:i+1]
                if ancestor in self.cell_suids:
                    self.cell_suids = list(set(self.cell_suids) - set([suid]))

    def compress(self):
        # compress
        if self.kind == 'rHEALPix':
            compressor = self._rhealpix_compress
        else:
            raise NotImplementedError
        compressor()


    def order(self):
        if self.kind == 'rHEALPix':
            orderer = self._rhealpix_order
        else:
            raise NotImplementedError
        orderer()

    def _rhealpix_compress(self):
        """Compresses a list of Cell IDs"""
        upper_cells = {}
        for cell in self.cell_suids:
            upper_cells.setdefault(cell[:-1], []).append(cell)
        compressed_cells = []
        for k, v in upper_cells.items():
            if len(v) == 9:
                compressed_cells.append(k)
            else:
                compressed_cells.extend(v)
        self.cell_suids = compressed_cells

    def _rhealpix_order(self):
        """Orders a list of Cell IDs"""
        # convert the first char of each Cell ID to a string representation of a number
        nums = [str(zero_cells.index(x[0])) + ''.join([str(i) for i in x[1:]]) for x in self.cell_suids]
        # sort numerical Cell IDs as per integers
        s = sorted(nums, key=int)
        # convert first character back to a letter
        self.cell_suids = [zero_cells[int(x[0])] + x[1:] for x in s]

class Cell:
    """
    DGGS Cell class.
    Provides:
    - core attributes of a cell: neighbours
    - validation
    This cell class is only aware of the cell suid and it's relationship to neighbouring suid.
    It does *not* include the rHEALPix library to facilitate conversion of DGGS Cells to conventional geometries.
    Can be extended to support validation and compression for different CRS's
    Currently supports rHEALPix
    """
    def __init__(self, suid, kind='rHEALPix', crs='auspix'):
        assert isinstance(suid, (str, tuple))
        self.crs = crs
        self.kind = kind
        self.N = N_crs[crs]
        if isinstance(suid, str):
            self.suid = self.suid_from_str(suid)
        elif isinstance(suid, tuple):
            self.suid = suid
        self.validate()

    def __repr__(self):
        return ''.join([str(i) for i in self.suid])

    def suid_from_str(self, suid_str):
        """
        Creates a cell tuple from a string
        """
        # first character should be in the zero cells
        assert suid_str[0] in zero_cells
        # any remaining characters should be digits in the range 0..N^2
        if len(suid_str) > 1:
            for i in suid_str[1:]:
                assert int(i) in range(N_crs[self.crs]**2)
        return tuple([suid_str[0]] + [int(i) for i in suid_str[1:]])

    def validate(self):
        if self.kind == 'rHEALPix':
            format_validator = self._rhealpix_validator
        else:
            raise NotImplementedError
        format_validator()

    def _rhealpix_validator(self):
        assert self.suid[0] in zero_cells
        if len(self.suid) > 1:
            for digit in self.suid[1:]:
                assert digit in range(9)

    def atomic_neighbours(self):
        # atomic neighbours created from rhealpix
        # TODO memoize using code below
        n3_atomic_neighbours = {3: {'O': {'left': 'R', 'right': 'P', 'down': 'S', 'up': 'N'}, 'P': {'left': 'O', 'right': 'Q', 'down': 'S', 'up': 'N'}, 'Q': {'left': 'P', 'right': 'R', 'down': 'S', 'up': 'N'}, 'R': {'left': 'Q', 'right': 'O', 'down': 'S', 'up': 'N'}, 'N': {'down': 'O', 'right': 'P', 'up': 'Q', 'left': 'R'}, 'S': {'up': 'O', 'right': 'P', 'down': 'Q', 'left': 'R'}, 0: {'left': 2, 'right': 1, 'up': 6, 'down': 3}, 1: {'left': 0, 'right': 2, 'up': 7, 'down': 4}, 2: {'left': 1, 'right': 0, 'up': 8, 'down': 5}, 3: {'left': 5, 'right': 4, 'up': 0, 'down': 6}, 4: {'left': 3, 'right': 5, 'up': 1, 'down': 7}, 5: {'left': 4, 'right': 3, 'up': 2, 'down': 8}, 6: {'left': 8, 'right': 7, 'up': 3, 'down': 0}, 7: {'left': 6, 'right': 8, 'up': 4, 'down': 1}, 8: {'left': 7, 'right': 6, 'up': 5, 'down': 2}}}
        return n3_atomic_neighbours[N_crs[self.crs]]

        # north_square = south_square = 0
        #
        # N=3
        # # Taken from the rHEALPix DGGS repository
        #
        # # Initialize atomic neighbour relationships among suid.
        # # Dictionary of up, right, down, and left neighbours of
        # # resolution 0 suid and their subcells 0--(N_side**2 -1),
        # # aka the atomic neighbours.
        # # Based on the layouts
        # #
        # #   0
        # #   1 2 3 4   (but folded into a cube) and
        # #   5
        # #
        # #   0 1 2
        # #   3 4 5
        # #   6 7 8   (example for N_side=3).
        # #
        # an = {}
        # # neighbours of zero_cells[1], ..., zero_cells[4]
        # an[zero_cells[1]] = {
        #     "left": zero_cells[4],
        #     "right": zero_cells[2],
        #     "down": zero_cells[5],
        #     "up": zero_cells[0],
        #     }
        # an[zero_cells[2]] = {
        #     "left": zero_cells[1],
        #     "right": zero_cells[3],
        #     "down": zero_cells[5],
        #     "up": zero_cells[0],
        #     }
        # an[zero_cells[3]] = {
        #     "left": zero_cells[2],
        #     "right": zero_cells[4],
        #     "down": zero_cells[5],
        #     "up": zero_cells[0],
        #     }
        # an[zero_cells[4]] = {
        #     "left": zero_cells[3],
        #     "right": zero_cells[1],
        #     "down": zero_cells[5],
        #     "up": zero_cells[0],
        #     }
        # # neighbours of zero_cells[0] and zero_cells[5] depend on
        # # volues of north_square and south_square, respectively.
        # nn = north_square
        # an[zero_cells[0]] = {
        #     "down": zero_cells[(nn + 0) % 4 + 1],
        #     "right": zero_cells[(nn + 1) % 4 + 1],
        #     "up": zero_cells[(nn + 2) % 4 + 1],
        #     "left": zero_cells[(nn + 3) % 4 + 1],
        #     }
        # ss = south_square
        # an[zero_cells[5]] = {
        #     "up": zero_cells[(ss + 0) % 4 + 1],
        #     "right": zero_cells[(ss + 1) % 4 + 1],
        #     "down": zero_cells[(ss + 2) % 4 + 1],
        #     "left": zero_cells[(ss + 3) % 4 + 1],
        #     }
        #
        # # neighbours of 0, 1, ..., N**2 - 1.
        # for i in range(N ** 2):
        #     an[i] = {
        #         "left": i - 1,
        #         "right": i + 1,
        #         "up": (i - N) % N ** 2,
        #         "down": (i + N) % N ** 2,
        #         }
        # # Adjust left and right edge cases.
        # for i in range(0, N ** 2, N):
        #     an[i]["left"] = an[i]["left"] + N
        # for i in range(N - 1, N ** 2, N):
        #     an[i]["right"] = an[i]["right"] - N

    def neighbours_suids(self, include_diagonals=False):
        if include_diagonals:
            raise NotImplementedError('Not yet implemented')
        neighbours = []
        for direction in ("up", "down", "left", "right"):
            neighbours.append(self.neighbour(direction))
        return set([i.suid for i in neighbours])

    def neighbour(self, direction):
        an = self.atomic_neighbours()
        suid = self.suid
        N = self.N
        neighbour_suid = []
        up_border = set(range(N))
        down_border = set([(N - 1) * N + i for i in range(N)])
        left_border = set([i * N for i in range(N)])
        right_border = set([(i + 1) * N - 1 for i in range(N)])
        border = {
            "left": left_border,
            "right": right_border,
            "up": up_border,
            "down": down_border,
            }
        crossed_all_borders = False
        # Scan from the back to the front of suid.
        for i in reversed(list(range(len(suid)))):
            n = suid[i]
            if crossed_all_borders:
                neighbour_suid.append(n)
            else:
                neighbour_suid.append(an[n][direction])
                if n not in border[direction]:
                    crossed_all_borders = True
        neighbour_suid.reverse()
        # neighbour = Cell(self.rdggs, neighbour_suid)
        neighbour = neighbour_suid

        # Second, rotate the neighbour if necessary.
        # If self is a polar cell and neighbour is not, or vice versa,
        # then rotate neighbour accordingly.
        self0 = suid[0]
        neighbour0 = neighbour_suid[0]
        if (
                (self0 == zero_cells[5] and neighbour0 == an[self0]["left"])
                or (self0 == an[zero_cells[5]]["right"] and neighbour0 == zero_cells[5])
                or (self0 == zero_cells[0] and neighbour0 == an[self0]["right"])
                or (self0 == an[zero_cells[0]]["left"] and neighbour0 == zero_cells[0])
        ):
            # neighbour = neighbour.rotate(1)
            neighbour = self.rotate(neighbour_suid, 1)
        elif (
                (self0 == zero_cells[5] and neighbour0 == an[self0]["down"])
                or (self0 == an[zero_cells[5]]["down"] and neighbour0 == zero_cells[5])
                or (self0 == zero_cells[0] and neighbour0 == an[self0]["up"])
                or (self0 == an[zero_cells[0]]["up"] and neighbour0 == zero_cells[0])
        ):
            # neighbour = neighbour.rotate(2)
            neighbour = self.rotate(neighbour_suid, 2)
        elif (
                (self0 == zero_cells[5] and neighbour0 == an[self0]["right"])
                or (self0 == an[zero_cells[5]]["left"] and neighbour0 == zero_cells[5])
                or (self0 == zero_cells[0] and neighbour0 == an[self0]["left"])
                or (self0 == an[zero_cells[0]]["right"] and neighbour0 == zero_cells[0])
        ):
            # neighbour = neighbour.rotate(3)
            neighbour = self.rotate(neighbour_suid, 3)
        return Cell(tuple(neighbour))

    def rotate_entry(self, x, quarter_turns):
        """
        Let N = self.N_side and rotate the N x N matrix of subcell numbers ::

            0        1          ... N - 1
            N        N+1        ... 2*N - 1
            ...
            (N-1)*N  (N-1)*N+1  ... N**2-1

        anticlockwise by `quarter_turns` quarter turns to obtain a
        new table with entries f(0), f(1), ..., f(N**2 - 1) read from
        left to right and top to bottom.
        Given entry number `x` in the original matrix, return `f(x)`.
        Used in rotate().

        INPUT:

        - `x` - A letter from RHEALPixDGGS.cells0 or one of the integers
          0, 1, ..., N**2 - 1.
        - `quarter_turns` - 0, 1, 2, or 3.

        EXAMPLES::

            >>> c = Cell(RHEALPixDGGS(), ['P', 2])
            >>> print([c.rotate_entry(0, t) for t in range(4)])
            [0, 2, 8, 6]

        NOTES:

        Operates on letters from RHEALPixDGGS.cells0 too.
        They stay fixed under f.
        Only depends on `self` through `self.N_side`.
        """
        N = self.N
        # Original matrix of subcell numbers as drawn in the docstring.
        A = self.child_order()
        # Function (written as a dictionary) describing action of rotating A
        # one quarter turn anticlockwise.
        f = dict()
        for i in range(N):
            for j in range(N):
                n = A[(i, j)]
                f[n] = A[(j, N - 1 - i)]
        # Level 0 cell names stay the same.
        for c in zero_cells:
            f[c] = c

        quarter_turns = quarter_turns % 4
        if quarter_turns == 1:
            return f[x]
        elif quarter_turns == 2:
            return f[f[x]]
        elif quarter_turns == 3:
            return f[f[f[x]]]
        else:
            return x

    def rotate(self, suid, quarter_turns):
        """
        Return the suid of the cell that is the result of rotating this cell's
        resolution 0 supercell by `quarter_turns` quarter turns anticlockwise.
        Used in neighbour().
        """
        return [self.rotate_entry(x, quarter_turns) for x in suid]

    def child_order(self):
        child_order = {}
        for (row, col) in product(list(range(self.N)), repeat=2):
            order = row * self.N + col
            # Handy to have both coordinates and order as dictionary keys.
            child_order[(row, col)] = order
            child_order[order] = (row, col)
        return child_order