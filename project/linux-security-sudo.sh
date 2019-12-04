#!/usr/bin/env bash

set -e


#Prevent files from being deleted by mistake
mkdir /tmp/RECYCLE
echo "alias rm='mv -t /tmp/RECYCLE' " > /etc/profile.d/alias-rm.sh
echo "0 3 * * 7 /usr/bin/rm -rf /tmp/RECYCLE/*" > /var/spool/cron/tabs/root || echo "0 3 * * 7 /usr/bin/rm -rf /tmp/RECYCLE/*" > /var/spool/cron/root


#sudo
echo "poka ALL=(ALL) ALL" >> /etc/sudoers

