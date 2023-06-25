import math


def findBottomLeft(points: list):
    return min(points, key=lambda p: (p.x, p.y))


def slope(p1, p2):
    return 1.0*(p1.y-p2.y)/(p1.x-p2.x) if p1.x != p2.x else float('inf')


def sortCCW(points: list):
    bottom_left = findBottomLeft(points)
    points.pop(points.index(bottom_left))

    points.sort(key=lambda p: (slope(bottom_left, p), -p.y, p.x))
    points.insert(0, bottom_left)

    return points


def cross_product(p1, p2, p3):
    return (p2.x - p1.x) * (p3.y - p1.y) - (p2.y - p1.y) * (p3.x - p1.x)


def isLeftTurn(p1, p2, p3):
    return cross_product(p1, p2, p3) > 0


def grahamScan(points: list):
    start = findBottomLeft(points)
    sortCCW(points)
    convex_hull = [start]

    for p in points[1:]:
        convex_hull.append(p)

        while len(convex_hull) > 2 and not isLeftTurn(convex_hull[-3], convex_hull[-2], convex_hull[-1]):
            convex_hull.pop(-2)

    return [*convex_hull, start]
