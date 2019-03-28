#!/bin/bash
#copy this script to /etc/openvpn/ovpn_udp/ then run it as sudo
#give permissions
for i in *.ovpn; do
    echo "auth-user-pass pass.txt" >> $i
done