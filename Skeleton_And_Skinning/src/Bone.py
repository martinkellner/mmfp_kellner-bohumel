#class for operations with a bone (movement, rotation, creating)
class Bone:

    def __init__(self, parent, x0=0, x1=0, y0=0, y1=0):

        self._parent = parent
        self._children = []

        self._x0 = x0
        self._x1 = x1
        self._y0 = y0
        self._y1 = y1

    def __repr__(self):
        print(self._x0 + ' ' + self._x1 + '\n' + self._y0 + ' ' + self._y1)
