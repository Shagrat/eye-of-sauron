#!/bin/bash
set -o errexit
rm docs/swagger.json
git config --global user.email "nobody@nobody.org"
git config --global user.name "Travis CI"
python sleepless/swagger_export.py
cd docs
git add swagger.json
git commit -m "Update docs"
git push --force --quiet "https://${GITHUB_TOKEN}@$github.com/${GITHUB_REPO}.git" master > /dev/null 2>&1