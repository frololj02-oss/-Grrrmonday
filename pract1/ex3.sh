#!/bin/bash
text="${1:-Hello from RTU MIREA!}"
len=${#text}
line=$(printf "%*s" "$len" "" | tr ' ' '-')
echo "+-${line}-+"
echo "| ${text} |"
echo "+-${line}-+"