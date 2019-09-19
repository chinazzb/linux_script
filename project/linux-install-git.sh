#!/usr/bin/env bash
# install git

#failure  exit script
set -e

#work dir
workDir=`pwd`

#decompression
tar xvf ./software/git-*.tar.xz -C /tmp/
cd /tmp/git-*/ && ./configure --prefix=/usr/local/git && make && make install

#software link
ln -s /usr/local/git/bin/git /usr/bin/
