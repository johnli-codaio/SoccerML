#!/bin/bash - 
#===============================================================================
#
#          FILE: clear.sh
# 
#         USAGE: ./clear.sh 
# 
#   DESCRIPTION: 
# 
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: YOUR NAME (), 
#  ORGANIZATION: 
#       CREATED: 03/02/2016 08:47
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error

make clean
rm -f *.rcg *.rcl core.*
rm -fr Logfiles
mkdir -p Logfiles

