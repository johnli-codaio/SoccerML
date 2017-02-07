#!/bin/sh

cd data/
rcssserver server::fullstate_l=1 server::fullstate_r=1 server::kick_off_wait=10 server::auto_mode=1 &
wait 2

cd ../agent2d-3.1.1/src/
./start.sh -t agent2d &  
wait 2

cd ../../binaries/WrightEagle/
./start-local.sh     # this blocks, so it finishing signals the end of the game

echo Finished.
