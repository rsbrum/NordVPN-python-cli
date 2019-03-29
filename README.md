# OpenVPn/NordVPN Linux CLI interface 
This script will help you to quickly iterate through NordVPN's servers. It interfaces with the OpenVPN cli and uses NordVPN servers because it has the biggest amount of servers. 

You can use it to mask any pocess you want and avoid detection. 

If you want to automate it, remove the "await_user()" method in the VPN's "start()" method and the "input()" in the "main()" method in main.py. That way it won't wait for any user input.  


# To install - This will install OpenVPN and download NordVPN's ovpn files
```
sudo apt-get install openvpn
cd /etc/openvpn
sudo wget https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip
sudo apt-get install unzip
sudo unzip ovpn.zip
sudo rm ovpn.zip
```
 
## Check if ovpn files were extracted
`ls -al`

# To run
```
Set your NordVPN credentials in main.py
pip3 install psutil
python3 main.py 
```
