# THEANO_FLAGS='device=gpu,floatX=float32,lib.cnmem=0.5' python trainer.py 
from __future__ import print_function
import numpy as np
np.random.seed(42)  # for reproducibility

from keras.layers import Dense, Activation
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.optimizers import RMSprop


BATCH_SIZE = 128
SEQ_LENGTH = 50
SEQ_STEP = 5


# load data
rcgdata = np.loadtxt('data/parsedrcg.txt', delimiter=',')
rcldata = np.loadtxt('data/parsedrcl.txt', delimiter=',')

# match data rows, since parsed rcg and parsed rcl are not 1:1
time = 0
i_rcg = i_rcl = 0
while i_rcg < len(rcgdata) and i_rcl < len(rcldata):
  time_rcg = rcgdata[i_rcg,0]
  time_rcl = rcldata[i_rcl,0]

  if time_rcg == time_rcl and time_rcg > time:
    i_rcg += 1
    i_rcl += 1
    time = time_rcg
  elif time_rcg > time_rcl: # delete row
    rcldata = np.vstack((rcldata[:i_rcl], rcldata[i_rcl + 1:]))
  elif time_rcl > time_rcg: # delete row
    rcgdata = np.vstack((rcgdata[:i_rcg], rcgdata[i_rcg + 1:]))
  else:                     # something went wrong
    assert False

# chop off remaining rows and slice out time feature
rcldata = rcldata[:i_rcl, 1:11]    # player l1 is index 1 ~ 11
rcgdata = rcgdata[:i_rcg, 1:]

# number of features and size of output
n_features = rcgdata.shape[1]
n_output = rcldata.shape[1]

# actual training input and output
x = np.array([rcgdata[ind:ind + SEQ_LENGTH] for ind in xrange(0, len(rcgdata) - SEQ_LENGTH, SEQ_STEP)])
y = np.array([rcldata[ind + SEQ_LENGTH] for ind in xrange(0, len(rcldata) - SEQ_LENGTH, SEQ_STEP)])

# begin model
model = Sequential()
model.add(LSTM(128, input_shape=(SEQ_LENGTH, n_features)))
model.add(Dense(n_output))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer=RMSprop(lr=0.01))


def train(epochs):
  model.fit(x, y, batch_size=BATCH_SIZE, nb_epoch=epochs, verbose=1, shuffle=True)


if __name__ == '__main__':
  train(20)
