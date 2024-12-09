#!/bin/bash
# this file runs each machine on each test file

cd ..
for test_file in test/*; do
  echo "$(basename $test_file)" | python code/code_jmangion.py
  echo ""; echo ""
done

