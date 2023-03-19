import os, sys, subprocess
from datetime import date

class new_contest:
    def __init__(self):
        self.working_dir = None
        self.contest_dir = None
        self.resource_dir = None
        self.set_dir()
        
        self.pass_opt = -1
        self.pass_dir = None
        self.pass_gen = False
        self.pass_list = ['0'] * 40
        
        
    def set_dir(self):
        directory = None
        dir_set_success = False
        dir_append = ''
        dir_resource_num = 2
        
        print("Enter a path to contain the pc2-9.6.0 contest or enter 'default' to set path to 'C:'")
        response = input('>>> ').strip().lower()
        if response == 'default':
            directory = 'c:'
        else:
            directory = response
            
        while not os.path.exists(directory):
            print("Directory '"+directory+"' does not exist. Please retry")
            directory = input('>>> ').strip()
            if directory == 'default':
                directory = 'c:'
                
        self.check_existing_contest(directory)
        self.working_dir = directory
        self.contest_dir = os.path.join(self.working_dir+'\\','pc2-9.6.0')
        
        self.resource_dir = os.path.join(self.working_dir+'\\','pc2-9.6.0-resources-'+str(date.today().strftime("%m.%d.%Y")))
        while not dir_set_success:
            try:
                os.mkdir(self.resource_dir+dir_append)
                dir_set_success = True
            except FileExistsError:
                dir_append = '-' + str(dir_resource_num)
                dir_resource_num+=1
        
    def check_existing_contest(self, directory):
        proceed = None
        response = None
        if os.path.exists(directory+'\\pc2-9.6.0'):
            print("Existing contest 'pc2-9.6.0' exists. Please rename or remove existing contest.\n")
            print("After renaming or removing 'pc2-9.6.0', enter 'continue' to continue or 'exit' to exit.\n")
            while proceed is  None:
                response = input('>>> ').strip().lower()
                match response:
                    case 'continue':
                        proceed = True
                    case 'exit':
                        proceed = False
                    case default:
                        print("Invalid response. Enter 'continue' or 'exit'.")
                        
        if proceed is not None and not proceed:
            os.system('exit')
        else:
            print("Contest 'pc2-9.6.0' will be created in '"+directory+"'")
    
    def create_contest(self):
        isDefault = True
        self.password_options()
        
    def password_options(self):
        optionIsSelected = False
        passFileDirSet = False
        
        print("Please enter '/<#>' for the option <#> corresponding to the desired team password configuration:")
        print("\t/1 .............................. Generate passwords")
        print("\t/2 ....................... Use an existing text file")
        print("\t/3 ........................ Manually enter passwords")
        
        while not optionIsSelected:
            response = input('>>> ').strip()
            match response:
                case '/1':
                    self.pass_opt = 0
                    optionIsSelected = True
                case '/2':
                    self.pass_opt = 1
                    optionIsSelected = True
                case '/3':
                    self.pass_opt = 2
                    optionIsSelected = True
                case default:
                    print("Invalid response. Enter '/1', '/2', or '/3'.")
        
        optionIsSelected = False
        # 1. generate
        if self.pass_opt == 0:
            self.pass_gen = True
            #fin = open(os.path.join(self.resource_dir,'passwords.txt'), "w")
            
        # 2. use existing txt
        elif self.pass_opt == 1:
            print("Enter full directory folder of text file or enter 'default' to set password directory \nto the '"+self.resource_dir+"' folder")
            while not optionIsSelected:
                response = input('>>> ').strip().lower()
                if response == 'default':
                    self.pass_dir = self.resource_dir
                    optionIsSelected = True
                elif os.path.exists(response):
                    self.pass_dir = response
                    optionIsSelected = True
                else:
                    print("Directory does not exist or invalid response. Please enter 'default' or a valid directory.")
                    
            while not passFileDirSet:
                print("Move password text file to the specified folder.")
                print("Enter the name of the password text file including '.txt'.")
                pass_name = input('>>> ').strip()
                pass_text = os.path.join(self.pass_dir, pass_name)
                if os.path.exists(pass_text):
                    self.pass_dir = pass_text
                    passFileDirSet = True
                else:
                    print("File '"+pass_name+"' does not exist in '"+self.pass_dir+"'.")
                    print("Make sure the file is in the correct directory.\n")
            print("Password file set to '"+self.pass_dir+"'.")
                    
        # 3. mannualy type
        elif self.pass_opt == 2:
            response = None
            team1 = team2 = 'string'
            print("Enter 'manual' then the team number to begin and team number to end with manual password config.")
            print("Passwords will be generated before the first team and after the second team entered.\n")
            print("Enter 'default' to manually set passwords for all 40 teams.\n")
            print("[default/manual]")
            
            while response is None:
                response = input('>>> ').strip().lower()
                
                if response == 'manual':
                    while type(team1) == type('string'):
                        team1 = input("Team Number to begin manual password set: ").strip()
                        try:
                            team1 = int(team1)
                            if team1 > 40 or team1 <= 0:
                                print("Please enter a team number greater than 0 and less than or equal to 40.")
                                team1 = 'string'
                        except ValueError:
                            print("Not a valid team number.")
                            
                    while type(team2) == type('string'):
                        team2 = input("Team Number to end manual password set: ").strip()
                        try:
                            team2 = int(team2)
                            if team2 < team1:
                                print("Please enter a team number greater than or equal to",str(team1)+".")
                                team2 = 'string'
                        except ValueError:
                            print("Not a valid team number")
                    
                elif response == 'default':
                    team1 = 1
                    team2 = 40
                    
                else:
                    print("Enter 'default' or 'manual'.")
                    response = None
                
            for i in range(team1-1,team2):
                team_pass = '1'
                while len(team_pass) != 6:
                    team_pass = input("Password for team "+str(i+1)+": ").strip()
                    if len(team_pass) != 6:
                        print("Password must be 6 characters.")
                self.pass_list[i] = team_pass+'\n'
            
            # Implementation of writelines(self.pass_list) to passwords.txt will wait until password generation is complete
    
    """            
    def make_problems(self):
        print("Please put ")
        fin = open(os.path.join(self.resource_dir,'problem_list.txt'),"w")
        fin.write()
    """

def main():
    contest = new_contest()
    contest.create_contest()
    
if __name__ == '__main__':
    main()