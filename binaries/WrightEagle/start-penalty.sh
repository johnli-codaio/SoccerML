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
VERSION="Debug"
BINARY="WrightEagle"
TEAM_NAME="A"
LOG_DIR="Logfiles"
N="1"

while getopts  "h:p:v:b:t:l:n:" flag; do
    case "$flag" in
        h) HOST=$OPTARG;;
        p) PORT=$OPTARG;;
        v) VERSION=$OPTARG;;
        b) BINARY=$OPTARG;;
        t) TEAM_NAME=$OPTARG;;
        l) LOG_DIR=$OPTARG;;
        n) N=$OPTARG;;
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
T_PARAM="$N_PARAM -trainer on -force_penalty_mode on"

start_clients() {
    sleep 1.0
    ./start.sh -t A -v $VERSION -h $HOST -p $PORT -l $LOG_DIR -b $BINARY &

    sleep 0.1
    ./start.sh -t B -v $VERSION -h $HOST -p $PORT -l $LOG_DIR -b $BINARY &

    if [ $N -eq 1 ]; then
        rcssmonitor &
    fi

    sleep 0.1
    $CLIENT $T_PARAM &
}

run () {
    start_clients &
    rcssserver -server::coach=true -server::coach_w_referee=true -server::half_time=1 -server::extra_half_time=1 \
        -server::nr_extra_halfs=0 -server::nr_normal_halfs=0 -server::penalty_shoot_outs=true \
        -server::auto_mode=true -server::nr_normal_halfs=2
}

for i in `seq $N`; do
    run
done

