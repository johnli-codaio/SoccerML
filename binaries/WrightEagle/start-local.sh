#!/bin/bash

echo ""
echo "#######################################################################"
echo "#              WrightEagle 2D Soccer Simulation Team                  #"
echo "#                                                                     #"
echo "#                       Multi-Agent Systems Lab.                      #"
echo "#              School of Computer Science and Technology              #"
echo "#            University of Science and Technology of China            #"
echo "#                         Hefei, Anhui, China                         #"
echo "#                                                                     #"
echo "#                   Supervisor: Prof. Xiaoping Chen                   #"
echo "#   Team members: Aijun Bai, Guanghui Lu, Haochong Zhang              #"
echo "#                 Miao Jiang, Haibo Dai, Xiao Li                      #"
echo "#                                                                     #"
echo "#             Team website: http://wrighteagle.org/2d/                #"
echo "#######################################################################"
echo ""

HOST="localhost"
PORT="6000"
VERSION="."
BINARY="WrightEagle"
TEAM_NAME="WrightEagle"
TRAINING="false"
LOG_DIR="Logfiles"
PENALTY="false"

while getopts  "h:p:v:b:t:o:l:f" flag; do
    case "$flag" in
        h) HOST=$OPTARG;;
        p) PORT=$OPTARG;;
        v) VERSION=$OPTARG;;
        b) BINARY=$OPTARG;;
        t) TEAM_NAME=$OPTARG;;
        o) TRAINING=$OPTARG;;
        l) LOG_DIR=$OPTARG;;
        f) PENALTY="true";;
    esac
done

if [ $VERSION = "Debug" ]; then
    ulimit -c unlimited
    make debug
else
    make release
fi

CLIENT="./$VERSION/$BINARY"
mkdir $LOG_DIR 2>/dev/null
SLEEP_TIME=0.1

COACH_PORT=`expr $PORT + 1`
OLCOACH_PORT=`expr $PORT + 2`
N_PARAM="-team_name $TEAM_NAME -host $HOST -port $PORT -coach_port $COACH_PORT -olcoach_port $OLCOACH_PORT -log_dir $LOG_DIR"

G_PARAM="$N_PARAM -goalie on"
C_PARAM="$N_PARAM -coach on"
T_PARAM="$N_PARAM -trainer on"

if [ $PENALTY = "true" ]; then
    T_PARAM="$T_PARAM -force_penalty_mode on"
    rcssserver -server::coach=true -server::coach_w_referee=true -server::auto_mode=true -server::nr_normal_halfs=2 &
    sleep 0.5
    rcssmonitor &
fi

echo ">>>>>>>>>>>>>>>>>>>>>> $TEAM_NAME Goalie: 1"
$CLIENT $G_PARAM &
sleep 5

i=2
while [ $i -le 11 ]; do
	echo ">>>>>>>>>>>>>>>>>>>>>> $TEAM_NAME Player: $i"
	$CLIENT $N_PARAM &
	sleep $SLEEP_TIME
	i=`expr $i + 1`
done
sleep 3

echo ">>>>>>>>>>>>>>>>>>>>>> $TEAM_NAME Coach"
$CLIENT $C_PARAM &

sleep 1

if [ $PENALTY = "true" ] || [ $TRAINING = "true" ]; then
	sleep 5
	echo ">>>>>>>>>>>>>>>>>>>>>> $TEAM_NAME Trainer"
	$CLIENT $T_PARAM &
fi

wait

