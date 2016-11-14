''' Parses the .rcg file into a trainable format.

    To add more features, list the feature name in OUTPUT_PLAYE_FEATURES and
    uncomment the corresponding line in function parse().
'''
import sys

DELIM = ','
OUTPUT_FEATURES = [
  'time',
  'ball_pos_x',
  'ball_pos_y',
  'ball_vel_x',
  'ball_vel_y',
]
OUTPUT_PLAYERS = [
  'l1', 'l2', 'l3', 'l4', 'l5', 'l6', 'l7', 'l8', 'l9', 'l10', 'l11',
  'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'r9', 'r10', 'r11',
]
OUTPUT_PLAYER_FEATURES = [
  'pos_x',
  'pos_y',
  'vel_x',
  'vel_y',
  'angleBodyCommitted',
]


def parse(line):
  d = {}
  for group in line.strip().replace(')', '').split('('):
    if not group:
      continue

    tokens = group.strip().split(' ')

    if tokens[0] == 'show':
      d['time']                     = tokens[1]

    elif tokens[0] == 'b':
      d['ball_pos_x']               = tokens[1]
      d['ball_pos_y']               = tokens[2]
      d['ball_vel_x']               = tokens[3]
      d['ball_vel_y']               = tokens[4]

    elif tokens[0] == 'l' or tokens[0] == 'r':
      p = d[tokens[0] + str(tokens[1])] = {}
      # p['side']                     = tokens[0]
      # p['unum']                     = tokens[1]
      # p['playerTypeId']             = tokens[2]
      # p['state']                    = tokens[3]
      p['pos_x']                    = tokens[4]
      p['pos_y']                    = tokens[5]
      p['vel_x']                    = tokens[6]
      p['vel_y']                    = tokens[7]
      p['angleBodyCommitted']       = tokens[8]
      # p['angleNeckCommitted']       = tokens[9]
      # if len(tokens) > 10:
      #   p['arm_dest_X']             = tokens[10]
      #   p['arm_dest_Y']             = tokens[11]

    # elif tokens[0] == 'v':
    #   p['highQuality']              = tokens[1]
    #   p['visibleAngle']             = tokens[2]

    # elif tokens[0] == 's':
    #   p['stamina']                  = tokens[1]
    #   p['effort']                   = tokens[2]
    #   p['recovery']                 = tokens[3]
    #   p['staminaCapacity']          = tokens[4]

    # elif tokens[0] == 'f':
    #   p['getFocusTarget_side']      = tokens[1]
    #   p['getFocusTarget_unum']      = tokens[2]

    # elif tokens[0] == 'c':
    #   p['kickCount']                = tokens[1]
    #   p['dashCount']                = tokens[2]
    #   p['turnCount']                = tokens[3]
    #   p['catchCount']               = tokens[4]
    #   p['moveCount']                = tokens[5]
    #   p['turnNeckCount']            = tokens[6]
    #   p['changeViewCount']          = tokens[7]
    #   p['sayCount']                 = tokens[8]
    #   p['tackleCount']              = tokens[9]
    #   p['arm_getCounter']           = tokens[10]
    #   p['attentiontoCount']         = tokens[11]

  return d


def featurestring():
  string = '#' + DELIM.join(OUTPUT_FEATURES)
  for player in OUTPUT_PLAYERS:
    for feature in OUTPUT_PLAYER_FEATURES:
      string += DELIM + player + '.' + feature
  return string


def tostring(d):
  string = DELIM.join([d[f] for f in OUTPUT_FEATURES])
  for player in OUTPUT_PLAYERS:
    for feature in OUTPUT_PLAYER_FEATURES:
      string += DELIM + d[player][feature]
  return string


def parse_rcg(in_filename):
  with open(in_filename, 'r') as in_file:
    sequence = []
    for line in in_file:
      if line.startswith('(show '):
        d = parse(line)
        if int(d['time']) > len(sequence):
          sequence.append(tostring(d))
    return sequence


def write_sequence(sequence, out_filename, write_header=True):
  with open(out_filename, 'w') as out_file:
    if write_header:
      out_file.write(featurestring() + '\n')
    for t in sequence:
      out_file.write(t + '\n')


if __name__ == '__main__':
  if len(sys.argv) < 3:
    print 'Usage:  %s <in_file.rcg> <out_file.txt>' % sys.argv[0]
    sys.exit(-1)
  sequence = parse_rcg(sys.argv[1])
  write_sequence(sequence, sys.argv[2])
