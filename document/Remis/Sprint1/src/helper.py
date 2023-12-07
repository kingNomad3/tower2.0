## Module de geometrie 2D
##

import math


class Helper(object):
    no_id = 0
    
    def getAngledPoint(angle, longueur, cx, cy):
        x = (math.cos(angle) * longueur) + cx
        y = (math.sin(angle) * longueur) + cy
        return x, y

    getAngledPoint = staticmethod(getAngledPoint)

    def calcAngle(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        angle = (math.atan2(dy, dx))
        return angle

    calcAngle = staticmethod(calcAngle)

    def calcDistance(x1, y1, x2, y2):
        dx = abs(x2 - x1) ** 2
        dy = abs(y2 - y1) ** 2
        distance = math.sqrt(dx + dy)
        return distance

    calcDistance = staticmethod(calcDistance)
    
    @staticmethod
    def creer_id():
        Helper.no_id += 1
        return "id_" + str(Helper.no_id)