import math

def cross(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

def is_point_in_triangle(p, a, b, c):
    pa = (a[0] - p[0], a[1] - p[1])
    pb = (b[0] - p[0], b[1] - p[1])
    pc = (c[0] - p[0], c[1] - p[1])

    d1 = cross(pa, pb)
    d2 = cross(pb, pc)
    d3 = cross(pc, pa)

    neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

    check = not (neg and pos)

    return check


def is_ear(polygon, i):
    prev = polygon[i - 1]
    curr = polygon[i]
    next = polygon[(i + 1) % len(polygon)]

    v1 = (curr[0] - prev[0], curr[1] - prev[1])
    v2 = (next[0] - prev[0], next[1] - prev[1])

    if cross(v1, v2) <= 0:
        return False
    
    for point in polygon:
        if point != prev and point != curr and point != next:
            if is_point_in_triangle(point, prev, curr, next):
                return False
    
    return True


def ear_clipping_algorithm(polygon):
    triangles = []
    polygon = polygon[:]

    while len(polygon) > 3:
        for i in range(len(polygon)):
            if is_ear(polygon, i):
                prev = polygon[i - 1]
                curr = polygon[i]
                next = polygon[(i + 1) % len(polygon)]
                triangles.append((prev, curr, next))

                del polygon[i]
                break

    triangles.append((polygon[0], polygon[1], polygon[2]))
    return triangles

def project_polygon(axis, points):
    project = [axis[0] * point[0] + axis[1] * point[1] for point in points]
    return min(project), max(project)

def get_axes(vertices):
    axes = []
    for i in range(len(vertices)):
        p1 = vertices[i]
        p2 = vertices[(i + 1) % len(vertices)]
        edge = (p2[0] - p1[0], p2[1] - p1[1])
        axis = (-edge[1], edge[0])
        length = math.sqrt(axis[0] ** 2 + axis[1] ** 2)
        axis = (axis[0] / length, axis[1] / length)
        axes.append(axis)
    return axes


def SAT_detect_collision(poly1, poly2):
    axes1 = get_axes(poly1)
    axes2 = get_axes(poly2)

    for axis in axes1 + axes2:
        poly1_min, poly1_max = project_polygon(axis, poly1)
        poly2_min, poly2_max = project_polygon(axis, poly2)

        if poly1_max < poly2_min or poly2_max < poly1_min:
            return False
    return True

def collision_detection_concave(poly1, poly2):
    triangles1 = ear_clipping_algorithm(poly1)
    triangles2 = ear_clipping_algorithm(poly2)

    for triangle1 in triangles1:
        for triangle2 in triangles2:
            if SAT_detect_collision(triangle1, triangle2):
                return True
    return False

    

