import subprocess, os, time, logging, psutil

logger = logging.getLogger('root')

class Vpn(object):
    """
        Interfaces with OpenVPN through bash scripts and 
        manages its connection
    """
    def __init__(self):
        self.status = False
        self.pid = 0

    def start(self,server_address):
        """
            Creates the script directory,
            forms the server using *server_address*,
            creates the bash command using the script dir and server address,
            opens a new terminal and uses the created command,
            checks if the PID of the terminal has been written to a file,
            sets the VPN status to True
            if VPN status is false, throws an error
        """

        pid_path = os.path.dirname(os.path.realpath(__file__)) + '/scripts/pid.txt'
        script_path = os.path.dirname(os.path.realpath(__file__)) + '/scripts/test.sh'

        cmd = "gnome-terminal -e ' sh -c \"sudo echo $$ >> {}; {} {}; sleep 20\"'" \
            .format(pid_path, script_path, server_address)

        logger.debug('Pid path: {}'.format(pid_path))
        logger.debug('Script path: {}'.format(script_path))
        logger.debug("CMD: {}".format(cmd))

        try:
            logger.debug("Removing old PID file...")
            os.remove(pid_path)
        except:
            logger.warning("PID file was already removed or non existent!")
            pass

        logger.debug("Executing cmd...")
        subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE, 
                        stdout=subprocess.PIPE, shell=True)
        try:
            self.wait_for_user(0)       
        except:
            return

        if os.path.exists(pid_path):
            logger.debug("Getting PID file...")

            with open(pid_path, 'r') as file:
                self.pid = int(file.read())
                file.close()
                os.remove(pid_path)
                logger.debug("PID file removed!")

        else:
            logger.error("PID file wasn't created")
            raise Exception("Failed to get OpenVPN's PID")

        self.set_OpenVPN_status()
        
        if not self.status:
            logger.debug("VPN PID wasn't alive") 
            self.kill()
            raise Exception("OpenVPN connection failed")

    def wait_for_user(self, tries):
        tries += 1 
        is_running = False
        processName = 'openvpn'
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if processName.lower() in proc.name().lower():
                    is_running = True
                else: 
                    is_running = False
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        if not is_running:
            logger.debug("Checking for openvpn process")
            time.sleep(1)
            self.wait_for_user(tries)
        else:
            logger.debug("PID file was created...")
            pass

        if tries == 21:
            logger.error("User did not respond!")
            raise Exception("User did not respond!")
            

    def check_if_process_running(self, processName):
        #Iterate over the all the running process
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if processName.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        return False
    def set_OpenVPN_status(self):
        """
            Checks if the OpenVPN process is active
            It wasn't possible to find the exact PID so there is a 
            but it is usually 3 very close to the provided *pid*
            if both tests fail, OpenVPN is False
            else True
        """
        logger.debug("Setting VPN status...")
        flag = None
        
        try:
            os.kill(self.pid,0)
        except:
            flag = True

        if flag == True:
            logger.debug("VPN is offline...")
            self.status = False
            return

        logger.debug("VPN is online")
        self.status = True
        
    def is_vpn_online(self):
        return self.status
        
    def kill(self):
        """
            Kills any OpenVPN process and scripts spawned by the VPN
        """
        logger.debug("Killing VPN process")
        self.status = False
        
        try:
            os.system("sudo killall openvpn")
        except:
            logger.warning("No openvpn was found")
