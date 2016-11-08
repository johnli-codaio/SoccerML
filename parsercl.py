import sys
import shlex

RELEVANT_ACTIONS = {'turn', 'dash', 'move', 'kick'}

# Result format: [(time, subtime), 'action']
def parse_ref_action(line):
    times = parse_times_tuple(line[0])
    action = line[-1].strip("()")
    return (tuple(times), action)

# e.g. '1,2' -> (1, 2)
def parse_times_tuple(string):
    times = map(int, string.split(','))
    return tuple(times)

# e.g. "(dash 71.2 45)(turn -0.12)" -> [("dash", [71.2, 45]), (turn, [-0.12])]
def parse_player_actions(actions):
    actions_arr = actions.split(')(')
    # Strip '(' and ')'
    actions_arr = map(lambda x: x.strip('()'), actions_arr)
    parsed_actions = map(parse_player_single_action, actions_arr)
    return filter(lambda x: x is not None, parsed_actions)

# e.g. "(dash 71.2 45)"" -> ("dash", [71.2, 45])
def parse_player_single_action(string):
    str_arr = string.split()
    action_name = str_arr[0]
    if action_name not in RELEVANT_ACTIONS:
        return None

    args = map(float, str_arr[1:])
    return (action_name, args)

# e.g. "TEAM_A_3 -> (TEAM_A, 3)"
def parse_player_info(player_info):
    split_str = player_info.split('_')
    # Edge case: Team name contains '_'
    team = ''.join(split_str[:-1])
    person = split_str[-1]
    try:
        person = int(person)
    except ValueError:
        assert person == 'Coach'
    return team, person

# Returns parsed data as a dict
# Format: data[team_name][player_number or 'Coach'] -> [(time_tuple, [actions...]), ...]
#         OR data['ref'] -> [((time, subtime), 'action'), ...]
def parse_file(in_file):
    data = {'ref': []}

    for line in in_file:
        line_arr = line.strip().split(None, 2)
        if line_arr[1] == "(referee":
            data['ref'].append(parse_ref_action(line_arr))
        else:
            # Check assumptions
            assert(line_arr[1] == 'Recv')
            assert(len(line_arr) == 3)

            times = parse_times_tuple(line_arr[0])

            event = line_arr[2].split(': ')
            assert(len(event) == 2)
            team, player_num = parse_player_info(event[0])
            actions = parse_player_actions(event[1])

            if actions:
                data[team] = data.get(team, {})
                data[team][player_num] = data[team].get(player_num, [])
                data[team][player_num].append((times, actions))

    return data

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage:  %s <in_file.rcl> <out_file.txt>' % sys.argv[0]
        sys.exit(-1)

    with open(sys.argv[1], 'r') as in_file, open(sys.argv[2], 'w') as out_file:
        data = parse_file(in_file)
        out_file.write(str(data) + '\n')

  
