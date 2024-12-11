import math

def cross(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

def point_in_triangle(point, p1, p2, p3):
    v1 = (p1[0] - point[0], p1[1] - point[1])
    v2 = (p2[0] - point[0], p2[1] - point[1])
    v3 = (p3[0] - point[0], p3[1] - point[1])

    flag1 = cross(v1, v2)
    flag2 = cross(v2, v3)
    flag3 = cross(v3, v1)

    return not ((flag1 < 0) or (flag2 < 0) or (flag3 < 0)) and ((flag1 > 0) or (flag2 > 0) or (flag3 > 0))

def ear(vertices, vertice1, vertice2, vertice3):
    if cross((vertice2[0] - vertice1[0], vertice2[1] - vertice1[1]), (vertice3[0] - vertice1[0], vertice3[1] - vertice1[1])) > 0:
        for p in vertices:
            if p not in (vertice1, vertice2, vertice3):
                if point_in_triangle(p, vertice1, vertice2, vertice3):
                    return False
        return True
    return False

    
def ear_clipping_algorithm(vertices):
    result = []
    temp = vertices[:]

    while len(temp) > 3:
        for i in range(len(temp)):
            vertice1 = temp[i - 1]
            vertice2 = temp[i]
            vertice3 = temp[(i + 1) % len(temp)]
            if ear(vertices, vertice1, vertice2, vertice3):
                result.append((vertice1, vertice2, vertice3))
                del temp[i]

                break
    result.append((temp[0], temp[1], temp[2]))
    return result

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