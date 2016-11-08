import sys

def parse(line):
  d = {}
  for group in line.strip().replace(')', '').split('('):
    if not group:
      continue

    tokens = group.strip().split(' ')

    if tokens[0] == 'show':
      d['time']                     = int(tokens[1])

    elif tokens[0] == 'b':
      d['ball_pos_x']               = float(tokens[1])
      d['ball_pos_y']               = float(tokens[2])
      d['ball_vel_x']               = float(tokens[3])
      d['ball_vel_y']               = float(tokens[4])

    elif tokens[0] == 'l' or tokens[0] == 'r':
      p = d[tokens[0] + str(tokens[1])] = {}
      p['side']                     = str(tokens[0])
      p['unum']                     = int(tokens[1])
      # p['playerTypeId']             = int(tokens[2])
      # p['state']                    = str(tokens[3])
      p['pos_x']                    = float(tokens[4])
      p['pos_y']                    = float(tokens[5])
      p['vel_x']                    = float(tokens[6])
      p['vel_y']                    = float(tokens[7])
      # p['angleBodyCommitted']       = float(tokens[8])
      # p['angleNeckCommitted']       = float(tokens[9])
      # if len(tokens) > 10:
      #   p['arm_dest_X']             = float(tokens[10])
      #   p['arm_dest_Y']             = float(tokens[11])

    # elif tokens[0] == 'v':
    #   p['highQuality']              = str(tokens[1])
    #   p['visibleAngle']             = float(tokens[2])

    # elif tokens[0] == 's':
    #   p['stamina']                  = float(tokens[1])
    #   p['effort']                   = float(tokens[2])
    #   p['recovery']                 = float(tokens[3])
    #   p['staminaCapacity']          = float(tokens[4])

    # elif tokens[0] == 'f':
    #   p['getFocusTarget_side']      = str(tokens[1])
    #   p['getFocusTarget_unum']      = int(tokens[2])

    # elif tokens[0] == 'c':
    #   p['kickCount']                = str(tokens[1])
    #   p['dashCount']                = int(tokens[2])
    #   p['turnCount']                = int(tokens[3])
    #   p['catchCount']               = str(tokens[4])
    #   p['moveCount']                = float(tokens[5])
    #   p['turnNeckCount']            = float(tokens[6])
    #   p['changeViewCount']          = float(tokens[7])
    #   p['sayCount']                 = float(tokens[8])
    #   p['tackleCount']              = float(tokens[9])
    #   p['arm_getCounter']           = float(tokens[10])
    #   p['attentiontoCount']         = float(tokens[11])

  return d


def tostring(d):
  # TODO
  # convert dict d into a one-line string to be written to file for training
  return str(d)


if __name__ == '__main__':
  if len(sys.argv) < 3:
    print 'Usage:  %s <in_file.rcg> <out_file.txt>' % sys.argv[0]
    sys.exit(-1)

  in_file  = open(sys.argv[1], 'r')
  out_file = open(sys.argv[2], 'w')

  blacklist_time = 0
  for line in in_file:
    if line.startswith('(show '):
      d = parse(line)
      if d['time'] != blacklist_time:
        str_d = tostring(d)
        out_file.write(str_d + '\n')

    elif line.startswith('(playmode '):
      blacklist_time = int(line.split(' ')[1])

    else:
      print line.strip()
