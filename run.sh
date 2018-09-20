#!/bin/bash
python3 dependency_parse.py model en_ewt-ud-train.conll en_ewt-ud-dev.pos en_ewt-ud-dev.conll | tee log
