#!/usr/bin/env bash

currentDir=$(dirname "$0")

cd "$currentDir"

bundle exec jekyll serve

cd -
