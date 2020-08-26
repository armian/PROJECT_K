#!/bin/bash

#find ./ -name "*.sh" -print
#find ./ -name "weak*" -print
find ./ -name "*.sh" | xargs rm -fv 
find ./ -name "weak*"| xargs rm -fv
rm -fv ./hydra.restore
