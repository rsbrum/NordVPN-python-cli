import logging, os, random, time, requests
from os import walk
from vpn.vpn import Vpn

"""
2 windows 
one for the vpn  
one for the app status 

need openvpn install
need nordvpn's ovpn files downloaded
write tests
connect to a random server - done
iterate through servers - done 
"""
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

handler = logging.StreamHandler()
handler.setFormatter(formatter)

f_handler = logging.FileHandler('file.log')   
f_handler.setFormatter(formatter)
s_handler = logging.StreamHandler()
s_handler.setFormatter(formatter)

logger = logging.getLogger('root')
logger.setLevel(logging.DEBUG)
logger.addHandler(f_handler)
logger.addHandler(s_handler)

vpn = Vpn()

def main():
    if not check_ovpn_files():
        logger.error("Ovpn files were not found!")
        return  

    if vpn.is_vpn_online():
        logger.warning("VPN was already online...")
        vpn.kill()

    servers = get_ovpn_servers()
    start_vpn(servers)


def start_vpn(servers):
    logger.debug("Starting vpn process...")
    server_index = random.randint(1, len(servers))

    try:
        vpn.start(servers[server_index])
        time.sleep(4)
        check_server_connection()
        logger.info('Connected at: {}'.format(servers[server_index]))

    except Exception as e:        
        vpn.kill()
        logger.error('Failed to connect to: {}'.format(servers[server_index]))
        logger.debug(e)

    input("Press ENTER to connect to a different server / Ctrl + z to exit")
    logger.info("Restarting VPN...")        
    start_vpn(servers)
    

def get_ovpn_servers():
    ovpn_files_path = "/etc/openvpn/ovpn_udp/"
    servers = []
    logger.debug('Collecting servers addresses from {}'.format(ovpn_files_path))
    
    try:
        if not os.path.isdir(ovpn_files_path):
            raise Exception() 

        for (dirpath, dirnames, filenames) in walk(ovpn_files_path):
            servers.extend(filenames)
            break
    except:
        logger.error("Failed to collect addresses! Check if NordVPN's ovpn files were installed." )

    return servers

def check_ovpn_files():
    logger.debug("Checking ovpn files...")
    ovpn_files_path = "/etc/openvpn/ovpn_udp/"
    flag = os.path.exists(ovpn_files_path)

    if not flag: 
        logger.error("Ovpn file were not found")
        raise Exception("Ovpn files directory does not exist")
    else:
        return True

def is_internet_on():
    try:
        logger.debug("Pinging https://google.com")
        requests.get('https://google.com', timeout=1)
    except Exception as e:
        logger.debug(e) 
        logger.error("Failed to ping https://google.com!")
        raise Exception("No internet")

def is_OpenVPN_installed():
    logger.debug("Checking ovpn files...")
    ovpn_files_path = "/etc/openvpn/ovpn_udp/"
    flag = os.path.exists(ovpn_files_path)

    if not flag: 
        logger.error("Ovpn file were not found")
        raise Exception("Ovpn files directory does not exist")
    else:
        return True

def check_server_connection():
    logger.info("Checking server connection...")
    errors = 0
    for x in range(3):
        try:
            time.sleep(0.5)
            is_internet_on()
        except:
            logger.warning("Server is not responding!")
            errors += 1
        
        if errors == 3:
            logger.error("Server did not respond!")
            raise Exception("Server didn't respond")

def create_auth_file(username, pwd):
    path = "/etc/openvpn/ovpn_udp/"
    cmd = "cd {}; echo $'{}\n{}'".format(path, username, pwd)


if __name__ == '__main__':
    main()
