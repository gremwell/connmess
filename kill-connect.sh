#!/bin/sh -x
ps ax | grep 'python3 connect' | grep -v grep | awk '{print $1}' | xargs kill
