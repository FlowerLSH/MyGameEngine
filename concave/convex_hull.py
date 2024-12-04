import concave

def cross_point(o, a, b):
    vector1 = (a[0] - o[0], a[1] - o[1])
    vector2 = (b[0] - o[0], b[1] - o[1])
    return concave.cross(vector1, vector2)


def convex_hull(points):
    points = sorted(points)
    lower, upper = [], []
    for point in points:
        while len(lower) >= 2 and cross_point(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    for point in reversed(points):
        while len(upper) >= 2 and cross_point(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]
