#!/bin/sh
set -eu

mkdir -p docs
cp README.md docs/index.md
cp LICENSE docs/LICENSE.md

if [ -f CHANGELOG.md ]; then
    cp CHANGELOG.md docs/
fi

if [ -f CONTRIBUTING.md ]; then
    cp CONTRIBUTING.md docs/
fi
