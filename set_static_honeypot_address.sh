#!/bin/sh

# インターフェース名の取得
ip=$(which ip)
interface=$(ip route ls | \
    awk '/^default / {
          for(i=0;i<NF;i++) { if ($i == "dev") { print $(i+1); next; } }
         }'
        )

# setting_file="/etc/network/interfaces"
setting_file="test.txt"
json_honeypot_address=`cat static_honeypot_address.json`
configs=`echo ${json_honeypot_address} | jq '.configs'`
address=`echo ${configs} | jq -r .[$1].address`
netmask=`echo ${configs} | jq -r .[$1].netmask`
gateway=`echo ${configs} | jq -r .[$1].gateway`
dnsnameservers=`echo ${configs} | jq -r .[$1].dnsnameservers`


cat << EOF >> ${setting_file}

auto ${interface}
iface ${interface} inet static
address ${address}
netmask ${netmask}
gateway ${gateway}
dns-nameservers ${dnsnameservers}
EOF
