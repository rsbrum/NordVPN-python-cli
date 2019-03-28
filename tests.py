import os

def create_auth_files(username, pwd):
    #logger.info("Appending auth credentials to ovpn files...")
    path = "/etc/openvpn/ovpn_udp/"
    cmds = ["sudo echo '{}\n{}' > pass.txt".format(username, pwd), 
            "sudo cp pass.txt {}".format(path),
            "sudo chmod +x ./credentials.sh",
            "sudo cp credentials.sh {}".format(path),
            "cd {}; sudo ./credentials.sh".format(path)]
    
    for cmd in cmds:
        try:
            os.system(cmd)
        except:
            print("error")

create_auth_files('rnsbrum@gmail.com', 'Cel91476045!')