'''
Script works in any directory under C:\ root as long 
as pc2-9.6.0 is properly created and in C:\ base

only tested on localhost so far
run through cmd as admin
'''

import os
import subprocess

class pc2_instance:
    def __init__(self):
        self.bin_path = 'c:\pc2-9.6.0\\bin'
        self.set_working_path(self.bin_path)
        #self.open_teams = []
        self.server_proc = None
        self.admin_proc = None
        self.started = False
        
        self.ether_is_connected = False
        self.ether_port_name = ''
    
    def get_help(self):
        print("Ensure that 'pc2_runner.py' is executed with administrator\naccess on a Windows OS\n\n")
        print("To start 'Server' and 'Admin', enter 'start'\n")
        print("To open any PC2 batch file, enter the name of the file \nwithout the leading 'PC2' and trailing '.bat' extension\n")
        print("To transfer contest from 'wi-Fi' to Ethernet connection,\nenter '/c ethernet'.")
        print("To end the script, enter 'exit'\n")
    
    def set_working_path(self, path_name):
        os.chdir(path_name)
        
    def get_profiles(self):
        prof_path = os.path.join(self.bin_path, 'profiles')
        return os.listdir(prof_path)
        
    def start_contest(self):
        self.started = True
        
        server_path = os.path.join(self.bin_path, 'pc2server.bat')
        admin_path = os.path.join(self.bin_path, 'pc2admin.bat')
        
        self.toggle_firewall()
        self.yn_command('netsh interface ip set address name="wi-Fi" static 192.168.1.2 255.255.255.0 192.168.1.2')
        
        self.server_proc = subprocess.Popen(
            (server_path),
            stdout=subprocess.PIPE)
        output = self.server_proc.stdout
        
        profiles = self.get_profiles()
        done = False
        
        for line in output:
            for profile in profiles:
                if "profiles\\\\"+profile+"\\r\\n'" in str(line):
                    self.admin_proc = subprocess.Popen(
                        (admin_path),
                        stdout=subprocess.PIPE)
                    return
                    
    def run_other(self, other):
        if 'pc2'+other+'.bat' in os.listdir(self.bin_path):
            other_path = os.path.join(self.bin_path, 'pc2'+other+'.bat')
            subprocess.Popen((other_path))
        else:
            print("Command '"+other+"' does not exist.")
        
    def yn_command(self, cmd):
        done = False
        print("Running process '"+cmd+"'.")
        
        while not done:
            print('Confirm process [y/n]')
            response = input(">>> ").strip().lower()[0:1]
            match response:
                case 'y':
                    subprocess.run(cmd)
                    print("Process executed.")
                    done = True
                case 'n':
                    print("Cancelling call to '"+cmd+"'.")
                    done = True
                case default:
                    print("Invalid response.")
                    
    def toggle_firewall(self):
        count = 0
        done = False
        
        disp_firewall = subprocess.Popen(
            ("netsh Advfirewall show allprofiles"),
            stdout=subprocess.PIPE).stdout
        
        for line in disp_firewall:
            line = tuple(str(line).strip()[2:-5].split())
            if count % 17 == 3:
                if count // 17 == 0:
                    print('Domain Profile State: ',line[1])
                elif count // 17 == 1:
                    print('Private Profile State:',line[1])
                elif count // 17 == 2:
                    print('Public Profile State: ',line[1])
            count+=1
            
        while not done:
            print("Toggle Firewall State [on/off]")
            cmd = input(">>> ").strip().lower()
            if cmd == 'on' or cmd == 'off':
                subprocess.run("NetSh Advfirewall set allprofiles state "+cmd)
                print('All firewall profile states are now',cmd,'\n')
                done = True
            else:
                print("Invalid response.")
             
    def transfer_to_ethernet(self):
        print('Connect Ethernet')
        done = False
        validPort = False
        while not done:
            print("Transfer contest onto 'Ethernet' connection [y/n]")
            response = input('>>> ').strip().lower()
            match response:
                case 'y':
                    portName = self.check_ether_connection()
                    if portName == 'exit':
                        print('Exiting Ethernet connection process.')
                    else:
                        portNum = ''
                        while not validPort:
                            portNum = input("Enter IP port name for 'wi-Fi': ").strip()
                            try:
                                portNum = int(portNum)
                            except ValueError:
                                portNum = 'string'
                                
                            if portNum != 'string' and portNum > 0:
                                print('Invalid Port. Enter a valid number greater than 0.\n')
                            else:
                                validPort = True
                              
                        subprocess.run('netsh interface ip set address name="wi-Fi" static 192.168.1.'+portNum+' 255.255.255.0 192.168.1.'+portNum)
                        subprocess.run('netsh interface ip set address name="'+portName+'" static 192.168.1.2 255.255.255.0 192.168.1.2')
                        
                        self.ether_is_connected = True
                    done = True
                case 'n':
                    print('Transfer to Ethernet canceled.')
                    done = True
                case default:
                    print("Invalid response.\n")
                    print("Enter 'y' to transfer contest to 'Ethernet'.\nEnter 'n' to stay on 'wi-Fi' connection")

    def check_ether_connection(self):
        etherConnected = False
        portName = 'exit'
        i = 0
        max_index, address_index = 8193, -1
        etherConnections = []
        
        output = subprocess.Popen(('ipconfig'),
            stdout=subprocess.PIPE).stdout
        
        for line in output:
            line_list = str(line)[2:-5].strip().split()
            if 'Ethernet' in str(line) and 'adapter' in str(line):
                portName = ''
                temp = [word for word in line_list[2:]]
                
                for x in temp:
                    portName += str(x) + ' '
                portName = portName[0:-1]
                if portName[-1:] == ':':
                    portName = portName[0:-1]
                max_index = i+2
                
            if i == max_index:
                if 'Media disconnected' not in str(line):
                    address_index = max_index + 2
                else:
                    etherConnections.append((portName,'Media disconnected'))
            if i == address_index:
                etherConnections.append((portName, line_list[13]))
                
            i+=1
        
        if len(etherConnections) == 0:
            print("No Ethernet ports found. Stay on wi-Fi.")
        else:
            print("Enter '/<#>' to choose an Ethernet connection to transfer the contest to:")
            index = 1
            for e in etherConnections:
                print("\t/"+"index",e[0]+':',e[1])
                index+=1
            print()
            
            while not etherConnected:
                response = input('>>> ').strip()[1:]
                try:
                    response = int(response)
                    if response <= 0 or response > len(etherConnections):
                        print("Please choose one of the above options.")
                        response2 = None
                    else:
                        portName = etherConnections[response][1]
                        response2 = None
                        
                        print("Confirm contest transfer to '"+etherConnections[response][1]+" : "+portName+"' [y/n]")
                        while response2 == None:
                            response2 = input('>>> ').strip()
                            match response2:
                                case 'y':
                                    self.ether_port_name = portName
                                    return portName
                                case 'n':
                                    return 'exit'
                                case default:
                                    print("Enter 'y' to confirm transfer or 'n' to cancel.")
                                    response2 = None
                except ValueError:
                    print("Invalid Response. Enter '/<#>' based on above options.")
                    
        return 'exit'


def main():
    pc2i = pc2_instance()
    command = ''
    print("Enter '/h' for help.")
    
    while command != 'exit':
        command = input(">>> ").strip().lower()
        match command:
            case "start":
                pc2i.start_contest()
            case "exit":
                if pc2i.started:
                    pc2i.yn_command('netsh interface ip set address name="wi-Fi" dhcp')
                    if pc2i.ether_is_connected:
                        pc2i.yn_command('netsh interface ip set address name="'+pc2i.ether_port_name+'" dhcp')
                    pc2i.toggle_firewall()
                print("'pc2_runner.py' terminated")
            case "/c ethernet":
                pc2i.check_ether_connection()
            case "/h":
                pc2i.get_help()
            case default:
                pc2i.run_other(command)
                    
if __name__ == '__main__':
    main()