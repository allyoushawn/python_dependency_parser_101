#!/bin/bash

# self-implemented dependency parser
python3 scripts/dependency_parse.py model data/en_ewt-ud-train.conll data/en_ewt-ud-dev.pos data/en_ewt-ud-dev.conll | tee log

# Run Stanford Parsers
python3 scripts/nltk_stanford_dependency_parser.py

# plot learning curves
python3  utils/plot_learning_curves.py

# Run analysis on self-implemented dependency parser
python3 error_analysis_sciripts/dependency_parse.py

# Run analysis on Stanford Parsers
python3 error_analysis_scripts/nltk_stanford_dependency_parser.py

# Plot the error analysis curves
python3 utils/plot_error_curve.py
