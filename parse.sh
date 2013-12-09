#!/bin/bash

file=$1

grep \<td\>  $file | awk -F'>' '{if ((NR % 5) == 1 ) print $3; if ((NR % 5) == 3) print $2 ; if  ((NR % 5) == 4 ) print $4  }'   | awk -F '<' '{print $1}' > ${file}_parsed
