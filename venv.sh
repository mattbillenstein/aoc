#!/bin/bash

rm -fR .venv
pypy3 -m venv .venv
source .venv/bin/activate

pip3 install sortedcontainers
