#!/usr/bin/env bash

set -x

autoflake \
    --remove-all-unused-imports \
    --recursive \
    --remove-unused-variables \
    --exclude=__init__.py \
    --in-place $*

isort \
    --multi-line=3 \
    --trailing-comma \
    --force-grid-wrap=0 \
    --combine-as \
    --line-width 90 \
    --recursive \
    --apply $*

black $* \
    --line-length 90 \
    --target-version py37 \
    --skip-string-normalization

vulture $* \
    --min-confidence 70 \
    --exclude=toolbox
