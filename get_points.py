keypointsMapping = ['Nose', 'Neck', 'R-Sho', 'R-Elb', 'R-Wr', 'L-Sho', 'L-Elb', 'L-Wr', 'R-Hip', 'R-Knee', 'R-Ank',
                    'L-Hip', 'L-Knee', 'L-Ank', 'R-Eye', 'L-Eye', 'R-Ear', 'L-Ear']
indicies = list(range(0, len(keypointsMapping)))

point_names_to_index = dict(zip(keypointsMapping, indicies))


def length_calculator(index):
    return index + 1


def from_point_name_to_index(point_name):
    return point_names_to_index[point_name]


def if_all_present_execute_function(points, not_present, execute):
    for point in points.values():
        if len(point) <= 0:
            return not_present
    return execute(points)


def getPointsFromName(decoded_data, point_names):
    points = {}
    for point_name in point_names:
        temp_point = getPointFromCamera(decoded_data, point_name)
        points[point_name] = temp_point
    return points


def getPointFromCamera(decoded_data, point_name):
    index = from_point_name_to_index(point_name)
    if len(decoded_data) >= length_calculator(index):
        return decoded_data[index]
    else:
        return []


def extract_x_and_y(point_from_camera):
    x, y, *_ = point_from_camera
    return [x, y]
