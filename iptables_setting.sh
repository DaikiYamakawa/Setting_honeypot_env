#!/bin/sh

# インターフェース名の取得
ip=$(which ip)
interface=$(ip route ls | \
    awk '/^default / {
          for(i=0;i<NF;i++) { if ($i == "dev") { print $(i+1); next; } }
         }'
        )

iptables -t nat -A POSTROUTING -s 192.168.11.0/24 -j MASQUERADE
iptables -t nat -A PREROUTING -i $interface -p tcp --dport 22 -j REDIRECT --to-port 2222
iptables -t nat -A PREROUTING -i $interface -p tcp --dport 23 -j DNAT --to-destination 192.168.11.1:23
iptables -A INPUT -i $interface -p tcp --dport 2222 -j ACCEPT
iptables -A INPUT -m conntrack --ctstate INVALID -j DROP
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# forwarding IN/OUTの制限設定
iptables -A FORWARD -i $interface -j ACCEPT
iptables -A FORWARD -o $interface -m limit --limit 5/m --limit-burst 1 -j ACCEPT

# ping(ICMP) ACCEPT
# iptables -I INPUT -p icmp --icmp-type 0 -j ACCEPT
# iptables -I INPUT -p icmp --icmp-type 8 -j ACCEPT

iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# 試験中に永続化すると死にます
sudo /etc/init.d/netfilter-persistent save
