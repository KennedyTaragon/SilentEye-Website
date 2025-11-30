#!/bin/bash

# Generates directory tree, excluding node_modules and staticfiles, and saves output to tree.txt
tree -I 'Documents|docs|staticfiles|migrations|__pycache__' > tree.txt
