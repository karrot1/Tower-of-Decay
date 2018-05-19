class Rect:
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

    def findmiddle(self, a, b):
        return int((a+b)/2)

    def center(self):
        center_x = self.findmiddle(self.x1, self.x2)
        center_y = self.findmiddle(self.y1, self.y2)
        return(center_x, center_y)

    def intersect(self, other):
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)