#!/usr/bin/env bash


set -e
set -x


# setup nodejs
set +x
echo 'init nvm'
source "$(pwd -P)/nvm/nvm.sh"
nvm use default
set -x


# build static files
npm install -g npm
npm install --no-save 
npm rebuild
rm -rf dist
npm run lint
npm run build


# copy static files
rsync -a dist/static/vue-test www/static/
cp -a dist/vue-test/index.html www/vue-test/index.html

set +x
echo -e '\e[01;32m✓ Done.\e[0m'
