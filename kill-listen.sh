#!/bin/sh -x
ps ax | grep 'python3 listen' | grep -v grep | awk '{print $1}' | xargs kill
