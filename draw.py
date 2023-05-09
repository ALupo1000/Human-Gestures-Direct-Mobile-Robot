import cv2
inputSize = (432, 368)


def set_text(frame, text='THIS IS SAMPLE TEXT', font=cv2.FONT_HERSHEY_SIMPLEX, bottom_left_corner_position=(0, 100), fontScale=2, fontColor=(0, 0, 0), thickness=3, lineType=2):
    cv2.putText(frame, text,
                bottom_left_corner_position,
                font,
                fontScale,
                fontColor,
                thickness,
                lineType)


def scale(point, scaleW, scaleH):
    return int(point[0] * scaleW), int(point[1] * scaleH)


def rgb_to_bgr(r, g, b):
    return (b, g, r)


def draw_line(frame, points, color):
    scaleW = frame.shape[1] / inputSize[0]
    scaleH = frame.shape[0] / inputSize[1]
    cv2.line(frame, scale(points[0], scaleW, scaleH), scale(
        points[1], scaleW, scaleH), color, 30)


def in_range(start, end, angle):
    return angle >= start and angle <= end


def set_functionality_based_on_degree_range(angle, raised, given_range):
    for current in given_range:
        start, end = current['degree_range']
        if angle >= start and angle <= end and raised:
            current['function']()


def set_functionality_based_on_degree_range_from_both_sides(left_angle, right_angle, given_range_joint, raised_left, raised_right):
    for current in given_range_joint:
        start, end = current['degree_range']
        if in_range(start, end, left_angle) and in_range(start, end, right_angle) and raised_left and raised_right:
            current['function']()


def is_in_degree_range(angle, raised, given_range):
    for current in given_range:
        start, end = current['degree_range']
        if angle >= start and angle <= end and raised:
            return True
    return False


def is_in_degree_range_from_both_sides(left_angle, right_angle, given_range_joint, raised_left, raised_right):
    for current in given_range_joint:
        start, end = current['degree_range']
        if in_range(start, end, left_angle) and in_range(start, end, right_angle) and raised_left and raised_right:
            return True
    return False


'''
scaleW = frame.shape[1] / inputSize[0]
    scaleH = frame.shape[0] / inputSize[1]

            cv2.line(frame, scale(points[0], scaleW, scaleH), scale(
                points[1], scaleW, scaleH), current['color'], 30)
    for current in below:
        start, end = current['degree_range']
        if angle >= start and angle <= end and not raised:
            cv2.line(frame, scale(points[0], scaleW, scaleH), scale(
                points[1], scaleW, scaleH), current['color'], 30)
            current['function']()
'''
