#!/usr/bin/env bash
set -e

source /etc/profile.d/mysql.sh || echo "this used db2 database"
dbName=$1
dbUser=$2
dbPass=$3
dbGrantHost=$4
mysql -uroot -p -e "create database $dbName"
mysql -uroot -p -e "grant all on $dbName.* to $dbUser@'$dbGrantHost' identified by '$dbPass'"
