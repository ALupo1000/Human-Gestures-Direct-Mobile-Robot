import os
import time
from get_points import extract_x_and_y, getPointsFromName, if_all_present_execute_function
from translate import from_neck_origin, from_neck_origin_to_angle
from draw import set_text, set_functionality_based_on_degree_range, set_functionality_based_on_degree_range_from_both_sides, draw_line, rgb_to_bgr, is_in_degree_range, is_in_degree_range_from_both_sides
from lock import put_on_queue_to_execute
from pydub import AudioSegment
from pydub.playback import play
from threading import Thread
import pyautogui

dir_absolute_path = os.path.dirname(os.path.abspath(__file__))
left_sound = AudioSegment.from_file(
    os.path.join(dir_absolute_path, 'left.mp3'))
right_sound = AudioSegment.from_file(
    os.path.join(dir_absolute_path, 'right.mp3'))
stop_sound = AudioSegment.from_file(
    os.path.join(dir_absolute_path, 'stop.mp3')
)
forward_sound = AudioSegment.from_file(
    os.path.join(dir_absolute_path, 'forward.mp3')
)
is_playing_left = False
is_playing_right = False
is_playing_stop = False
is_playing_forward = False

left = {
    'points': [],
    'angle': {
        'wrist': 0,
        'elbow': 0
    },
    'raised': False
}

right = {
    'points': [],
    'angle': {
        'wrist': 0,
        'elbow': 0
    },
    'raised': False
}


def root_wrapper(*executions):
    for execute in executions:
        execute()


def play_left_sound():
    global is_playing_left
    play(left_sound)
    is_playing_left = False


def play_right_sound():
    global is_playing_right
    play(right_sound)
    is_playing_right = False


def play_stop_sound():
    global is_playing_stop
    play(stop_sound)
    is_playing_stop = False


def play_forward_sound():
    global is_playing_forward
    play(forward_sound)
    is_playing_forward = False


def left_direction_wrapper():
    global is_playing_left
    pyautogui.keyUp('a')
    if not is_playing_left:
        is_playing_left = True
        Thread(target=play_left_sound, args=()).start()
        pyautogui.keyDown('a')
        time.sleep(0.5)
        pyautogui.keyUp('a')


def right_direction_wrapper():
    global is_playing_right
    pyautogui.keyUp('d')
    if not is_playing_right:
        is_playing_right = True
        Thread(target=play_right_sound, args=()).start()
        pyautogui.keyDown('d')
        time.sleep(0.5)
        pyautogui.keyUp('d')


def stop_direction_wrapper():
    global is_playing_stop
    if not is_playing_stop:
        is_playing_stop = True
        Thread(target=play_stop_sound, args=()).start()


def forward_direction_wrapper():
    global is_playing_forward
    if not is_playing_forward:
        is_playing_forward = True
        Thread(target=play_forward_sound, args=()).start()
        pyautogui.keyDown('w')
        time.sleep(0.5)
        pyautogui.keyUp('w')


def line_drawing_wrapper(frame, points, color):
    if len(points) >= 2:
        draw_line(frame, points, color)


def onNewFrame(frame, source):
    pass


def onShowFrame(frame, source):
    above_left = [
        {
            'degree_range': (0, 10),
            'function': lambda: root_wrapper(lambda: left_direction_wrapper(), lambda: line_drawing_wrapper(frame, left['points'], rgb_to_bgr(0, 255, 0)))
        },
        {
            'degree_range': (21, 30),
            'function': lambda: line_drawing_wrapper(frame, left['points'], rgb_to_bgr(0, 255, 0))
        },
        {
            'degree_range': (31, 90),
            'function': lambda: line_drawing_wrapper(frame, left['points'], rgb_to_bgr(0, 0, 255))
        }
    ]

    below_left = [
        {
            'degree_range': (1, 10),
            'function': lambda: line_drawing_wrapper(frame, left['points'], rgb_to_bgr(255, 0, 0))
        },
        {
            'degree_range': (21, 30),
            'function': lambda: line_drawing_wrapper(frame, left['points'], rgb_to_bgr(0, 255, 0))
        },
        {
            'degree_range': (31, 90),
            'function': lambda: line_drawing_wrapper(frame, left['points'], rgb_to_bgr(0, 0, 255))
        }
    ]

    above_right = [
        {
            'degree_range': (0, 10),
            'function': lambda: root_wrapper(lambda: right_direction_wrapper(), lambda: line_drawing_wrapper(frame, right['points'], rgb_to_bgr(0, 255, 0)))
        },
        {
            'degree_range': (21, 30),
            'function': lambda: line_drawing_wrapper(frame, right['points'], rgb_to_bgr(0, 255, 0))
        },
        {
            'degree_range': (31, 90),
            'function': lambda: line_drawing_wrapper(frame, right['points'], rgb_to_bgr(0, 0, 255))
        }
    ]

    below_right = [
        {
            'degree_range': (1, 10),
            'function': lambda: line_drawing_wrapper(frame, right['points'], rgb_to_bgr(255, 0, 0))
        },
        {
            'degree_range': (21, 30),
            'function': lambda: line_drawing_wrapper(frame, right['points'], rgb_to_bgr(0, 255, 0))
        },
        {
            'degree_range': (31, 90),
            'function': lambda: line_drawing_wrapper(frame, right['points'], rgb_to_bgr(0, 0, 255))
        }
    ]

    above_joint = [
        {
            'degree_range': (0, 80),
            'function': lambda: root_wrapper(lambda: stop_direction_wrapper(), lambda: set_text(frame, text='STOP MOVING', bottom_left_corner_position=(
                0, 700), fontColor=(255, 0, 0)))
        },
        {
            'degree_range': (100, 150),
            'function': lambda: root_wrapper(lambda: forward_direction_wrapper(), lambda: set_text(frame, text='MOVING FORWARD', bottom_left_corner_position=(
                0, 700), fontColor=(255, 0, 0)))
        }
    ]

    set_text(frame, text=f'LEFT DEGREES WRIST: {left["angle"]["wrist"]}', bottom_left_corner_position=(
        0, 100), fontColor=(0, 255, 100))
    set_text(frame, text=f'RIGHT DEGREE WRIST: {right["angle"]["wrist"]}', bottom_left_corner_position=(
        0, 200), fontColor=(0, 255, 100))
    set_text(frame, text=f'LEFT DEGREES ELBOW: {left["angle"]["elbow"]}', bottom_left_corner_position=(
        0, 300), fontColor=(0, 255, 100))
    set_text(frame, text=f'RIGHT DEGREE ELBOW: {right["angle"]["elbow"]}', bottom_left_corner_position=(
        0, 400), fontColor=(0, 255, 100))

    if is_in_degree_range_from_both_sides(left['angle']['elbow'], right['angle']['elbow'], above_joint, left['raised'], right['raised']):
        put_on_queue_to_execute(lambda: is_in_degree_range_from_both_sides(left['angle']['elbow'], right['angle']['elbow'], above_joint, left['raised'], right['raised']), 'ABOVE_JOINT', lambda: set_functionality_based_on_degree_range_from_both_sides(
            left['angle']['elbow'], right['angle']['elbow'], above_joint, left['raised'], right['raised']))
    else:
        if is_in_degree_range(left['angle']["wrist"], left['raised'], above_left):
            put_on_queue_to_execute(lambda: is_in_degree_range(left['angle']["wrist"], left['raised'], above_left), 'ABOVE_LEFT', lambda: set_functionality_based_on_degree_range(
                left['angle']["wrist"], left['raised'], above_left))
        elif is_in_degree_range(right['angle']['wrist'], right['raised'], above_right):
            put_on_queue_to_execute(lambda: is_in_degree_range(right['angle']['wrist'], right['raised'], above_right), 'ABOVE_RIGHT', lambda: set_functionality_based_on_degree_range(
                right['angle']['wrist'], right['raised'], above_right))
        else:
            if is_in_degree_range(right['angle']['wrist'], right['raised'], above_right):
                put_on_queue_to_execute(lambda: is_in_degree_range(right['angle']['wrist'], right['raised'], above_right), 'BELOW_LEFT', lambda: set_functionality_based_on_degree_range(
                    left['angle']["wrist"], not left['raised'], below_left))
            elif is_in_degree_range(right['angle']['wrist'], not right['raised'], below_right):
                put_on_queue_to_execute(lambda: is_in_degree_range(right['angle']['wrist'], not right['raised'], below_right), 'BELOW_RIGHT', lambda: set_functionality_based_on_degree_range(
                    right['angle']['wrist'], not right['raised'], below_right))

    if left['raised']:
        set_text(frame, text='THE LEFT HAND IS BEING RAISED', bottom_left_corner_position=(
            0, 500), fontColor=(0, 0, 255))
    else:
        set_text(frame, text='THE LEFT HAND IS BEING LOWERED', bottom_left_corner_position=(
            0, 500), fontColor=(0, 255, 0))

    if right['raised']:
        set_text(frame, text='THE RIGHT HAND IS BEING RAISED', bottom_left_corner_position=(
            0, 600), fontColor=(0, 0, 255))
    else:
        set_text(frame, text='THE RIGHT HAND IS BEING LOWERED', bottom_left_corner_position=(
            0, 600), fontColor=(0, 255, 0))


def onNn(nn_packet, decoded_data):
    left_translated_from_name_to_points = getPointsFromName(
        decoded_data[0], ['Neck', 'L-Sho', 'L-Wr', 'L-Elb'])
    left['points'] = if_all_present_execute_function(left_translated_from_name_to_points, [], lambda left_points: [
        extract_x_and_y(left_points['L-Sho'][0]), extract_x_and_y(left_points['L-Wr'][0])])
    left['angle']['wrist'] = if_all_present_execute_function(left_translated_from_name_to_points, 0, lambda left_points: from_neck_origin_to_angle(
        left_points['Neck'][0], left_points['Neck'][0], left_points['L-Sho'][0], left_points['L-Wr'][0]))
    left['angle']['elbow'] = if_all_present_execute_function(left_translated_from_name_to_points, 0, lambda left_points: from_neck_origin_to_angle(
        left_points['Neck'][0], left_points['L-Elb'][0], left_points['L-Sho'][0], left_points['L-Wr'][0]))
    left['raised'] = if_all_present_execute_function(
        left_translated_from_name_to_points, False, lambda left_points:  from_neck_origin(
            left_points['Neck'][0], left_points['Neck'][0], left_points['L-Sho'][0], left_points['L-Wr'][0])[2][1] < 0)

    right_translated_from_name_to_points = getPointsFromName(
        decoded_data[0], ['Neck', 'R-Sho', 'R-Wr', 'R-Elb'])
    right['points'] = if_all_present_execute_function(right_translated_from_name_to_points, [], lambda right_points: [
        extract_x_and_y(right_points['R-Sho'][0]), extract_x_and_y(right_points['R-Wr'][0])])
    right['angle']['wrist'] = if_all_present_execute_function(right_translated_from_name_to_points, 0, lambda right_points: from_neck_origin_to_angle(
        right_points['Neck'][0], right_points['Neck'][0], right_points['R-Sho'][0], right_points['R-Wr'][0]))
    right['angle']['elbow'] = if_all_present_execute_function(right_translated_from_name_to_points, 0, lambda right_points: from_neck_origin_to_angle(
        right_points['Neck'][0], right_points['R-Elb'][0], right_points['R-Sho'][0], right_points['R-Wr'][0]))
    right['raised'] = if_all_present_execute_function(
        right_translated_from_name_to_points, False, lambda right_points:  from_neck_origin(
            right_points['Neck'][0], right_points['Neck'][0], right_points['R-Sho'][0], right_points['R-Wr'][0])[2][1] < 0)


def onReport(report):
    pass


def onSetup(*args, **kwargs):
    pass


def onTeardown(*args, **kwargs):
    pass


def onIter(*args, **kwargs):
    pass
