#!/bin/bash
SUM=0
for i in {1..10} ; do
  START=$(date +%s%3N)
  python ./src/main.py
  END=$(date +%s%3N)
  EXETIME=$((END - START))
  echo ${EXETIME}
  SUM=$((SUM + EXETIME))
done
MEANTIME=$((SUM / 10.000))
echo ${MEANTIME}