#!/usr/bin/env bash
# install docker

#failure  exit script
set -e

tar zxvf ./software/docker-*.tgz -C /usr/bin/
gourpadd docker
cp ./conf/docker/* /usr/lib/systemd/system/

systemctl enable docker



