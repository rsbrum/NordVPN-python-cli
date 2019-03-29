import logging
import os
import random
import time
import requests
from os import walk
from vpn.vpn import Vpn

formatter = logging.Formatter(
    fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

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

##################################################
#     Provide your OpenVPN credentials here      #
#                                                #
username = 'email@email.com'                     # 
password = 'password'                            #
#                                                #
#                                                #
##################################################

def main():
    if not check_ovpn_files():
        logger.error("Ovpn files were not found!")
        logger.info("Download ovpn files from the link in the github page!")
        return

    if vpn.is_vpn_online():
        logger.warning("VPN was already online...")
        vpn.kill()

    if not check_auth_files():
        create_auth_files(username, password)

    servers = get_ovpn_servers()
    start_vpn(servers)


def start_vpn(servers):
    """
        Starts the OpenVPN with the 
        provided list of servers from 
        NordVPN's ovpn files
    """
    logger.info("Starting vpn process...")
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
    """
        Gets server addresses from ovpn files 
    """
    ovpn_files_path = "/etc/openvpn/ovpn_udp/"
    servers = []
    logger.debug(
        'Collecting servers addresses from {}'.format(ovpn_files_path))
    logger.info(
        'Collecting server addresses'
    )
    try:
        if not os.path.isdir(ovpn_files_path):
            raise Exception()

        for (dirpath, dirnames, filenames) in walk(ovpn_files_path):
            servers.extend(filenames)
            break
    except:
        logger.error(
            "Failed to collect addresses! Check if NordVPN's ovpn files were installed.")

    return servers


def check_ovpn_files():
    """
        Checks if OVPN files have been downloaded
    """
    logger.debug("Checking ovpn files...")
    ovpn_files_path = "/etc/openvpn/ovpn_udp/"
    flag = os.path.exists(ovpn_files_path)

    if not flag:
        logger.error("Ovpn file were not found")
        return False
    else:
        return True


def is_internet_on():
    """
        Pings google to check if the chosen server is responding
    """
    try:
        logger.debug("Pinging https://google.com")
        requests.get('https://google.com', timeout=1)
    except Exception as e:
        logger.debug(e)
        logger.error("Failed to ping https://google.com!")
        raise Exception("No internet")


def is_OpenVPN_installed():
    """
        Checks if OpenVPN has been installed
    """
    logger.debug("Checking ovpn files...")
    ovpn_files_path = "/etc/openvpn/"
    flag = os.path.exists(ovpn_files_path)

    if not flag:
        logger.error("Ovpn file were not found")
        raise Exception("Ovpn files directory does not exist")
    else:
        return True


def check_server_connection():
    """ 
        Tests the server connection 3 times
        if it is not responding, raises an exception
    """
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


def check_auth_files():
    """
        Checks if the pass.txt file has been created
        if it wasn't, OpenVPN will ask for credentials
    """
    logger.info('Checking auth files...')
    path = "/etc/openvpn/ovpn_udp/pass.txt"

    if os.path.isfile(path):
        return True

    return False


def create_auth_files(username, pwd):
    """
        If pass.txt wasn't created,
        creates pass.txt with provided username and password
        copies pass.txt to ovpn files directory
        gives permission to the shell script
        to append credentials to each ovpn file
        executes the shell script
    """
    logger.info('Creating auth files...')
    #logger.info("Appending auth credentials to ovpn files...")
    path = "/etc/openvpn/ovpn_udp/"
    cmds = ["sudo echo '{}\n{}' > pass.txt".format(username, pwd),
            "sudo cp pass.txt {}".format(path),
            "sudo chmod +x ./credentials.sh",
            "sudo cp credentials.sh {}".format(path),
            "cd {}; sudo ./credentials.sh".format(path)]

    for cmd in cmds:
        os.system(cmd)

    logger.info('Auth appended to ovpn files!')


if __name__ == '__main__':
    main()
