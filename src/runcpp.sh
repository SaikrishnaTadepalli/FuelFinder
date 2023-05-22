#!/bin/sh
# Compiles and runs C++ source code. A corresponding file
# ending with .in will be used as input, if present

set -eu

if [ $# -ne 1 ] || [ -z "$1" ]
then
  echo "Usage: $0 SOURCE"
  exit 1
fi

executable=$(mktemp -t run-cpp.XXXXXXXXXX)
trap 'rm $executable' EXIT

green=$(tput setaf 2)
normal=$(tput sgr0)

echo "${green}Compiling...${normal}"
g++ -o "$executable" -std=c++17 -O3                     \
    -Wall -Wextra -Wwrite-strings -Wno-parentheses      \
    -Wpedantic -Warray-bounds -Weffc++                  \
    "$1"

echo "${green}Running...${normal}"
input=${1%.*}.in
if [ -f "$input" ]
then exec <"$input"
fi

"$executable"