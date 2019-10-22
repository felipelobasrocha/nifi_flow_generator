from enum import Enum

class CreateLocation:

    x = 0.0
    y = 0.0
    type = 1
    count = 0
    distance = 0

    def __init__(self, x, y, type, distance=300):
        self.x = x
        self.y = y
        self.type = type
        self.distance = distance

    def create(self):
        if self.type == LocationType.ZIGZAG:
            self.zigzag()
        elif self.type == LocationType.ROUNDABOUT:
            self.roundabout()
        else:
            self.line()

        self.count += 1

        return (self.x, self.y)

    def roundabout(self):
        if self.count > 12:
            self.y -= self.distance
        if self.count > 8:
            self.x -= self.distance
        elif self.count > 4:
            self.y += self.distance
        else:
            self.x += self.distance

    def zigzag(self):
        self.x += self.distance

        if self.count & 1:
            self.y += self.distance
        else:
            self.y -= self.distance

    def line(self):
        self.x += self.distance

class LocationType(Enum):
    LINE = 1
    ZIGZAG = 2
    ROUNDABOUT = 3
