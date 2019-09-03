#!/bin/bash

code=$(find . -name "*.py" | grep -v "main\.py" | grep -v "grove\.py" | xargs cat | grep -vP "^(import|from) ")
imports="$(find . -name "*.py" | grep -v "main\.py" | grep -v "grove\.py" | xargs cat | grep -P "^(import|from) " | sort | uniq)"

echo "$imports" > grove.py
echo "$code" >> grove.py
