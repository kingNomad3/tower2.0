class Chemin():
    def __init__(self, parent):
        self.parent = parent
        self.pivots = [[150, 0], [150, 450], [330, 450], [330, 120], [840, 120], [840, 240], [570, 240], [570, 450], [860, 450]]
        self.segments = []
        self.temp = self.pivots[0]
        self.creer_segments(self.pivots)


    def creer_segments(self, pivots):
        for i in pivots[1:]:
            self.segments.append([self.temp, i])
            self.temp = i