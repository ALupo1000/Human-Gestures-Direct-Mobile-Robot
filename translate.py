import numpy as np


def translate_point(origin, point):
    origin_x, origin_y = origin
    point_x, point_y = point
    return [point_x - origin_x, point_y - origin_y]


def from_neck_origin_to_angle(*points):
    first, second, third = from_neck_origin(*points)
    return get_angle_from_triangulation(first, second, third)


def from_neck_origin(neck, *other):
    neck_x, neck_y, *_ = neck
    translated_other = []
    for point in other:
        x, y, *_ = point
        translated_other.append(translate_point((neck_x, neck_y), (x, y)))
    return translated_other


def get_angle_from_triangulation(start, point_a, point_b):
    try:
        start_a = np.array(start)
        point_a_a = np.array(point_a)
        point_b_a = np.array(point_b)
        point_a_a_minus_start_a = point_a_a - start_a
        point_b_a_minus_start_a = point_b_a - start_a
        cosine_angle = np.dot(point_a_a_minus_start_a, point_b_a_minus_start_a) / (
            np.linalg.norm(point_a_a_minus_start_a) * np.linalg.norm(point_b_a_minus_start_a))
        angle = np.arccos(cosine_angle)
        return round(np.degrees(angle))
    except ValueError:
        return 0

