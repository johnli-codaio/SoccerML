"""Parses the .rcl file into a trainable format."""

import sys

DELIM = ','

OUTPUT_PLAYERS = [
    'l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7', 'l8', 'l9', 'l10', 'l11',
    'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11',
]

# 'turn', 'dash', 'move', and 'kick' are 1 if the action was performed,
# and 0 otherwise.
OUTPUT_PLAYER_FEATURES = [
    "turn", "turn_angle", "dash", "dash_power", "move",
    "move_x", "move_y", "kick", "kick_power", "kick_angle"
]

RELEVANT_ACTIONS = {
    'turn', 'dash', 'move', 'kick'
}

# Result format: [(time, subtime), "action"]
def parse_ref_action(line):
    times = parse_times_tuple(line[0])
    action = line[-1].strip("()")
    return (tuple(times), action)

# "time,subtime" -> (time, subtime)
def parse_times_tuple(string):
    times = map(int, string.split(','))
    return tuple(times)

# "(move1 arg1 arg2)(move2 arg1)" -> [(move1, [arg1, arg2]), (move2, [arg2])]
def parse_player_actions(actions):
    actions_arr = actions.split(')(')
    # Strip '(' and ')'
    actions_arr = map(lambda x: x.strip('()'), actions_arr)
    parsed_actions = map(parse_player_single_action, actions_arr)
    return filter(lambda x: x is not None, parsed_actions)

# "(move arg1 arg2)" -> (move, [arg1, arg2])
def parse_player_single_action(string):
    str_arr = string.split()
    action_name = str_arr[0]
    if action_name not in RELEVANT_ACTIONS:
        return None

    args = map(float, str_arr[1:])
    if action_name == "dash":
        args = args[:1]
    return (action_name, args)

# e.g. "TEAM_A_3 -> (TEAM_A, 3)"
# Coach is assigned player number 0.
def parse_player_info(player_info):
    split_str = player_info.split('_')
    # Edge case: Team name contains '_'
    team = ''.join(split_str[:-1])
    person = split_str[-1]
    try:
        person = int(person)
    except ValueError:
        assert person == 'Coach'
        person = 0
    return team, person

# Return whether a team is team 'l' or 'r'
# by looking at the .rcl file name.
def get_side(team_name, in_filename):
    assert(team_name in in_filename)
    versus_index = in_filename.index("-vs-")
    if in_filename.index(team_name) < versus_index:
        return 'l'
    return 'r'

# Returns parsed data as a matrix
def parse_rcl(in_filename):
    data = {} # data[time][player_id] = array of actions
    ref_actions = []

    with open(in_filename, 'r') as in_file:
        for line in in_file:
            line_arr = line.strip().split(None, 2)
            if line_arr[1] == "(referee":
                ref_actions.append(parse_ref_action(line_arr))
            else:
                assert(line_arr[1] == 'Recv')
                assert(len(line_arr) == 3)

                time, subtime = parse_times_tuple(line_arr[0])

                # Ignore if not in play
                if subtime != 0:
                    continue

                player_info, player_actions = line_arr[2].split(': ')

                team_name, player_num = parse_player_info(player_info)

                player_id = get_side(team_name, in_filename)  + str(player_num)
                actions = parse_player_actions(player_actions)

                if actions:
                    data[time] = data.get(time, {})
                    data[time][player_id] = data[time].get(player_id, [])
                    data[time][player_id].extend(actions)

    return get_matrix(data), ref_actions

# Takes in a dictionary of data and converts it into a matrix.
# matrix[time][move_index] = val
def get_matrix(data):
    matrix = [None] # t=0 is None since time begins at t=1
    end_time = max(data.keys())
    for _ in range(end_time):
        matrix.append(empty_vector())

    for time in data:
        vector = matrix[time]

        for player in data[time]:
            assert player in OUTPUT_PLAYERS
            player_index = OUTPUT_PLAYERS.index(player) * len(OUTPUT_PLAYER_FEATURES)

            for move_name, args in data[time][player]:
                move_index = player_index + OUTPUT_PLAYER_FEATURES.index(move_name)
                vector[move_index] = 1.0

                for i in range(len(args)):
                    vector[move_index + i + 1] = args[i]
    return matrix

def empty_vector():
    vector_length = len(OUTPUT_PLAYERS) * len(OUTPUT_PLAYER_FEATURES)
    return [0.0 for _ in range(vector_length)]

def featurestring():
    string = "#time"
    for player in OUTPUT_PLAYERS:
        for feature in OUTPUT_PLAYER_FEATURES:
            string += DELIM + player + '.' + feature
    return string

def write_matrix_to_file(matrix, out_filename):
    with open(out_filename, 'w') as out_file:
        out_file.write(featurestring() + "\n")
        for i in range(1, len(matrix)):
            line = str(i)
            line += DELIM + DELIM.join(map(str, matrix[i]))
            out_file.write(line + "\n")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage:  %s <in_file.rcl> <out_file.txt>' % sys.argv[0]
        sys.exit(-1)
    in_filename = sys.argv[1]
    out_filename = sys.argv[2]
    matrix, ref_actions = parse_rcl(in_filename)
    print ref_actions
    write_matrix_to_file(matrix, out_filename)