class Entity:
    #a generic object to represent basicaly everything
    def __init__(self, x, y, char, color):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
    def move(self, dx, dy):
        #moves entity by amount
        self.x += dx
        self.y += dy