class Chemin():
    def __init__(self, parent, choixTableau):
        self.parent = parent
        ratio = 70
        self.pivots = [[[150, 0], [150, 450], [330, 450], [330, 120], [840, 120], [840, 240], [570, 240], [570, 450], [860, 450]],
                        [[0, 200], [300, 200], [300, 100], [600, 100], [600, 500], [700, 500], [700, 100], [200, 400], [900, 400]],
                       [[130- ratio, 0], [180- ratio, 100], [330- ratio, 100], [330- ratio, 200], [280- ratio, 300], [180- ratio, 400], [230- ratio, 500], [280- ratio, 550], [380- ratio, 590],
                        [510- ratio,590], [600- ratio,500], [530- ratio,350], [680- ratio,250], [700- ratio,550] ,[930- ratio,220], [935- ratio,220]]]

        self.segments = []
        self.temp = self.pivots[choixTableau][0]
        self.creer_segments(self.pivots[choixTableau])

    def creer_segments(self, pivots):
        for i in pivots[1:]:
            self.segments.append([self.temp, i])
            self.temp = i
