#!/bin/sh

echo '-----Making Honeypot Environment-----'
sudo apt update
sudo apt -y upgrade
sudo apt -y install tshark
sudo apt -y install qemu
sudo apt -y install bridge-utils
sudo apt -y install iptables-persistent
sudo apt -y install tmux
sudo apt -y install git-core
sudo apt -y install build-essential
sudo apt -y install libssl-dev
sudo apt -y install libncurses5-dev
sudo apt -y install unzip
sudo apt -y install gawk
sudo apt -y install zlib1g-dev
sudo apt -y install subversion
sudo apt -y install mercurial
sudo apt -y install python-2.7
sudo apt -y install python-twisted
sudo apt -y install python-mysqldb
sudo apt -y install python-geoip
sudo apt -y install python-watchdog
sudo apt -y install vim
sudo apt -y install jq
sudo apt -y install traceroute



