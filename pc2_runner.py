'''
Script works in any directory under C:\ root as long 
as pc2-9.6.0 is properly created and in C:\ base

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
        
        self.wiFi_not_DHCP = False
        self.ether_not_DHCP = False
        self.ether_full_name = ''
    
    def get_help(self):
        print("Ensure that 'pc2_runner.py' is executed with administrator\naccess on a Windows OS\n\n")
        print("To start 'Server' and 'Admin', enter 'start'\n")
        print("To open any PC2 batch file, enter the name of the file \nwithout the leading 'PC2' and trailing '.bat' extension\n")
        print("To transfer contest from 'wi-Fi' to Ethernet connection,\nenter '/ethernet'\n")
        print("To set server configuration, enter '/set ini'\n")
        print("To end the script, enter 'exit'\n")
    
    def set_working_path(self, path_name):
        os.chdir(path_name)
        
    def set_ini(self):
        #print("\nCurrent server configuration: '"+self.get_ini_config()+"'")
        self.get_ini_config()
        print("Choose server [ localhost / network ]")
        
        output = ''
        index = 0
        ini_path = os.path.join(self.bin_path, 'pc2v9.ini')
        # write_ini_path = os.path.join(self.bin_path, 'pc2v9_temp.ini')
        serv = None
        while serv is None:
            serv = input('>>> ').strip().lower()
            match serv:
                case 'localhost':
                    serv = 'localhost'
                case 'network':
                    serv = '192.168.1.2'
                case default:
                    print("Invalid server option. Enter 'localhost' or 'network'.\n")
                    serv = None
        
        # Options: default path / set path
        with open(ini_path, "r+") as f:
            for line in f:
                if index < 12 or index > 12:
                    output += str(line)
                else:
                    output += 'server='+serv+':50002\n'
                index += 1
            f.seek(0)
            f.write(output)
            f.truncate()
            
        print("Server set to '"+serv+"'.\n")
        
    def get_ini_config(self):
        serv = ''
        ini_path = os.path.join(self.bin_path, 'pc2v9.ini')
        index = 0
        
        f =  open(ini_path, "r")
        for line in f:
            if index == 12:
                serv = str(line)[7:-7]
            index += 1
        f.close()
        
        print("\nCurrent server:",serv)
            
        
    def get_profiles(self):
        prof_path = os.path.join(self.bin_path, 'profiles')
        return os.listdir(prof_path)
        
    def start_contest(self):
        self.started = True
        
        server_path = os.path.join(self.bin_path, 'pc2server.bat')
        admin_path = os.path.join(self.bin_path, 'pc2admin.bat')
        
        self.toggle_firewall()
        self.yn_command('netsh interface ip set address name="wi-Fi" static 192.168.1.2 255.255.255.0 192.168.1.2')
        self.wiFi_not_DHCP = True
        
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
            print("Running '"+"pc2"+other+".bat'.")
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
                    print("Process executed.\n")
                    done = True
                case 'n':
                    print("Cancelling call to '"+cmd+"'.\n")
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
        print('Ensure Ethernet is connected\n')
        done = False
        valid_IP = False
        
        while not done:
            print("Transfer contest onto Ethernet connection [y/n]")
            
            response = input('>>> ').strip().lower()
            match response:
                case 'y':
                    ether_name = self.check_ether_connection()
                    if ether_name == 'exit':
                        print('Exiting Ethernet transfer process.')
                    else:
                        host_ID = ''
                        while not valid_IP:
                            host_ID = input("Enter IP host ID for 'wi-Fi': ").strip()
                            
                            try:
                                host_ID = int(host_ID)
                            except ValueError:
                                host_ID = 'string'
                                
                            if host_ID != 'string' and host_ID > 0:
                                valid_IP = True
                            else:
                                print('\nInvalid IP host ID. Enter a valid number greater than 0.')
                                print('Ensure that host ID is available.\n')
                              
                        subprocess.run('netsh interface ip set address name="wi-Fi" static 192.168.1.'+str(host_ID)+' 255.255.255.0 192.168.1.'+str(host_ID))
                        subprocess.run('netsh interface ip set address name="'+str(ether_name)+'" static 192.168.1.2 255.255.255.0 192.168.1.2')
                        subprocess.run('netsh interface ip set address name="wi-Fi" dhcp')
                        
                        print("Transfer to",ether_name,"successful.")
                        self.ether_not_DHCP = True
                        
                    done = True
                    
                case 'n':
                    print('Transfer to Ethernet canceled.')
                    done = True
                    
                case default:
                    print("Invalid response.")
                    print("Enter 'y' to transfer contest to Ethernet.\nEnter 'n' to stay on 'wi-Fi' connection")

    def check_ether_connection(self):
        etherConnected = False
        ether_name = 'exit'
        max_index, address_index, i = 8193, -1, 0
        etherConnections = []
        
        output = subprocess.Popen(('ipconfig'),
            stdout=subprocess.PIPE).stdout
        
        for line in output:
            line_list = tuple(str(line)[2:-5].strip().split())
            
            if 'Ethernet' in str(line) and 'adapter' in str(line):
                ether_name = ''
                temp = [word for word in line_list[2:]]
                
                for x in temp:
                    ether_name += str(x) + ' '
                ether_name = ether_name[0:-1]
                
                if ether_name[-1:] == ':':
                    ether_name = ether_name[0:-1]
                max_index = i+2
                
            if i == max_index:
                if 'Media disconnected' not in str(line):
                    address_index = max_index + 2
                else:
                    etherConnections.append((ether_name,'Media disconnected'))
                    
            if i == address_index:
                etherConnections.append((ether_name, line_list[13]))
            i+=1
        
        if len(etherConnections) == 0:
            print("No Ethernet ports found. Stay on wi-Fi.")
        else:
            print("Enter '/<#>' to choose an Ethernet connection to transfer the contest to:\n")
            
            index = 1
            for e in etherConnections:
                str_btwn = ''
                len_btwn = 58 - len(e[0]) - len(e[1]) + 1
                
                spc_first = False
                if len(e[0]) % 2 == 0:
                    spc_first = True
                for integer in range(len(e[0]),len(e[0])+len_btwn):
                    add_val = '.'
                    if integer % 2 == 0:
                        add_val = ' '
                    str_btwn += add_val
                print("     /"+str(index),e[0]+str_btwn+e[1])
                index+=1
            print()
            
            while not etherConnected:
                response = input('>>> ').strip()
                if '/' not in response:
                    response = 'str'
                else:
                    response = response[1:]
                try:
                    response = int(response)
                    if response <= 0 or response > len(etherConnections):
                        print("Invalid Response. Enter '/<#>' based on above options.")
                    else:
                        ether_name = etherConnections[response-1][0]
                        ether_address = etherConnections[response-1][1]
                        response2 = None    
                        
                        print("Current status of Ethernet adapter",ether_name+":",ether_address)
                        print("Confirm contest transfer to '"+ether_name+" : "+ether_address+"' [y/n]")
                        
                        while response2 is None:
                            response2 = input('>>> ').strip()
                            match response2:
                                case 'y':
                                    self.ether_full_name = ether_name
                                    etherConnected = True
                                case 'n':
                                    ether_name = 'exit'
                                    etherConnected = True
                                case default:
                                    print("Enter 'y' to confirm transfer or 'n' to cancel.")
                                    response2 = None
        
                except ValueError:
                    print("Invalid Response. Enter '/<#>' based on above options.")
        
        return ether_name


def main():
    pc2i = pc2_instance()
    command = ''
    pc2i.set_ini()
    
    print("\nEnter '/h' for help.")
    
    while command != 'exit':
        command = input(">>> ").strip().lower()
        match command:
            case "start":
                pc2i.start_contest()
            case "exit":
                if pc2i.wiFi_not_DHCP:
                    pc2i.yn_command('netsh interface ip set address name="wi-Fi" dhcp')
                if pc2i.ether_not_DHCP:
                    pc2i.yn_command('netsh interface ip set address name="'+pc2i.ether_full_name+'" dhcp')
                if pc2i.started:
                    pc2i.toggle_firewall()
                print("'pc2_runner.py' terminated")
            case "/ethernet":
                pc2i.transfer_to_ethernet()
            case "/set ini":
                pc2i.set_ini()
            case "/h":
                pc2i.get_help()
            case default:
                pc2i.run_other(command)
                    
if __name__ == '__main__':
    main()