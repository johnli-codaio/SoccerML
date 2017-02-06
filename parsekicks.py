# Putting code related to extracting defense/offense sequences here;
# will probably need to refactor and clean up preprocess pipeline

import sys
from parsercl import *

# Returns dict where 
# key = an integer time step
# value = a list of players, each represented by a tuple (team name, unum),
# that kicked the ball at the given time step
def parse_kicks(in_filename):
    data = {}

    with open(in_filename, 'r') as in_file:
        for line in in_file:
            line_arr = line.strip().split(None, 2)

            if line_arr[1] == "(referee":
                continue
            else:
                # Check assumptions
                assert(line_arr[1] == 'Recv')
                assert(len(line_arr) == 3)

                time = parse_times_tuple(line_arr[0])[0]
		
	        event = line_arr[2].split(': ')
            assert(len(event) == 2)
            team, player_num = parse_player_info(event[0])
            actions = parse_player_actions(event[1])

            if actions:
                if "kick" in [a[0] for a in actions]:
                    if time in data:
                        data[time].append((team, player_num))
                    else:
                        data[time] = [(team, player_num)]

    return data

# Input dict:
# key = an integer time step
# value = a list of players, each represented by a tuple (team name, unum),
# that kicked the ball at the given time step
# Output list:
# [((start_time, end_time), team_with_ball)...]
# end_time is not inclusive
def get_possessions(kicks):
    max_time = max(kicks.keys())
    possess = None
    prev_kick_team = None
    prev_kick_time = None
    possessions = []
    start_time = 0

    for i in range(max_time):
        if i in kicks:
            if len(kicks[i]) == 1: # ignore times when both teams kick
                if kicks[i][0][0] != possess and prev_kick_team != possess:
                    # posession changed at prev_kick_time
                    possessions.append(((start_time, prev_kick_time), prev_kick_team))
                    possess = prev_kick_team
                    start_time = prev_kick_time
                prev_kick_team = kicks[i][0][0]
                prev_kick_time = i
        
    return possessions
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Usage:  %s <in_file.rcl> <out_file.txt>' % sys.argv[0]
        sys.exit(-1)
    in_filename = sys.argv[1]
    out_filename = sys.argv[2]
    kicks = parse_kicks(in_filename)
    print get_possessions(kicks)