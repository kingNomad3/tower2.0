class Chemin ():
    def __init__(self):
        self.grosseur_pixel = 40
        self.pivots = [[self.grosseur_pixel * 4, 0],
                       [self.grosseur_pixel * 4, self.grosseur_pixel * 16],
                       [self.grosseur_pixel * 12, self.grosseur_pixel * 16],
                       [self.grosseur_pixel * 12, self.grosseur_pixel * 4],
                       [self.grosseur_pixel * 28, self.grosseur_pixel * 4],
                       [self.grosseur_pixel * 28, self.grosseur_pixel * 10],
                       [self.grosseur_pixel * 18, self.grosseur_pixel * 10],
                       [self.grosseur_pixel * 18, self.grosseur_pixel * 16],
                       [self.grosseur_pixel * 28, self.grosseur_pixel * 16]]

        self.chemin = self.creer_segments()

    def creer_segments(self):
        segment = []
        debut = self.pivots[0]

        for i in self.pivots[1:]:
            segment.append([debut, i])
            debut = i

        return segment

