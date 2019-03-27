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
logger.setLevel(logging.INFO)
logger.addHandler(f_handler)
logger.addHandler(s_handler)

vpn = Vpn()

def main():
    servers = get_ovpn_servers()
    server_index = random.randint(1, len(servers))

    if vpn.is_vpn_online():
        logger.debug("Checking if VPN is online...")
        vpn.kill()

    try:
        vpn.start(servers[server_index])
        time.sleep(4)
        check_server_connection()
        logger.info('Connected at: {}'.format(servers[server_index]))
    except Exception as e:        
        vpn.kill()
        logger.error('Failed to connect to: {}'.format(servers[server_index]))
        logger.debug(e)
        main()
    
    input("Press ENTER to connect to a different server")
    logger.info("Restarting process...")
    main()

def get_ovpn_servers():
    mypath = "/etc/openvpn/ovpn_udp/"
    servers = []
    logger.debug('Collecting servers addresses from {}'.format(mypath))
    
    try:
        if not os.path.isdir(mypath):
            raise Exception() 

        for (dirpath, dirnames, filenames) in walk(mypath):
            servers.extend(filenames)
            break
    except:
        logger.error("Failed to collect addresses! Check if NordVPN's ovpn files were installed." )

    return servers

def is_internet_on():
    try:
        logger.debug("Pinging https://google.com")
        requests.get('https://google.com', timeout=1)
    except Exception as e:
        logger.debug(e) 
        logger.error("Failed to ping https://google.com!")
        raise Exception("No internet")

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
