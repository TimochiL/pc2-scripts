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
    
    def get_help(self):
        print("To start 'Server' and 'Admin', enter 'start'")
        print("To open any PC2 batch file, enter the name of the file \nwithout the leading 'PC2' and trailing '.bat' extension")
        print("To end the script, enter 'exit'")
        
    
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
        self.yn_command(True,'netsh interface ip set address name="wi-Fi" static 192.168.1.2 255.255.255.0 192.168.1.2')
        
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
        
    def yn_command(self, admin, cmd):
        done = False
        print("Running process '"+cmd+"'.")
        
        while not done:
            print('Confirm process [y/n]')
            response = input(">>> ").strip().lower()[0:1]
            match response:
                case 'y':
                    #subprocess.run(['cmd.exe','-command',"& {{Start-Process "+cmd+" -argumentlist '/k \"C:\WINDOWS\System32\WindowsPowerShell\\v1.0\"' -Verb Runas}}"])
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
        
    ''' FOR FUTURE IMPLEMENTATION (unfinished) (userdata.tsv only generated through client :c)
    def get_pass(self, account, team_num):
        if team_num not in self.open_teams:
            print('Team', team_num ,'is not available.\nPlease choose a different team:')
            for team in self.open_teams:
                print('\tTeam',team) 
        else:
            userdata_path = os.path.join(self.bin_path, 'userdata.tsv')
            with open(userdata_path) as fin:
                for line in fin.readlines():
                    user = tuple(line.strip().split())
                    if user[0] == account and user[1] == team_num:
                        print('Password:',user[-1])
    '''
    

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
                    pc2i.yn_command(True,'netsh interface ip set address name="wi-Fi" dhcp')
                    pc2i.toggle_firewall()
                print("'pc2_runner.py' terminated")
            case "/h":
                pc2i.get_help()
            case default:
                pc2i.run_other(command)
                    
if __name__ == '__main__':
    main()