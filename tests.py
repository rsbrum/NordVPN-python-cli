import os

def create_auth_files(username, pwd):
    #logger.info("Appending auth credentials to ovpn files...")
    path = "/etc/openvpn/ovpn_udp/"
    cmd = "cd {}; echo $'{}\n{}'".format(path, username, pwd)
    
    os.system(cmd)

create_auth_files('username', 'pwd')