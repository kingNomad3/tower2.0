class Chemin():
    def __init__(self, parent, choixTableau):
        self.parent = parent
        self.pivots = [[[150, 0], [150, 450], [330, 450], [330, 120], [840, 120], [840, 240], [570, 240], [570, 450], [860, 450]],
                        [[0, 200], [300, 200], [300, 100], [600, 100], [600, 500], [700, 500], [700, 100], [200, 400], [900, 400]],
                       [[150, 0], [200, 100], [350, 100], [350, 200], [300, 300], [200, 400], [250, 500], [300, 550], [400, 590], [550,590], [650,500], [450,350], [550,250], [1050,250]]]


        self.segments = []
        self.temp = self.pivots[choixTableau][0]
        self.creer_segments(self.pivots[choixTableau])


    def creer_segments(self, pivots):
        for i in pivots[1:]:
            self.segments.append([self.temp, i])
            self.temp = i


if __name__ == '__main__':
    chemin = Chemin()
    print("FIN")