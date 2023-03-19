# pc2_runner

#### 03.17.2023 

First version of pc2_runner.py with pc2 automation of internet and firewall config and contest startup.

#### 03.18.2023 

def get_pass FOR FUTURE IMPLEMENTATION (unfinished) (userdata.tsv only generated through client :c)

```python
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
```

Updated help message

# pc2_maker

#### 03.18.2023

Unfinished version of pc2_maker. Making and entering problem list has yet to be implemented.<br>
pc2_maker has path setting and team password options (generate, manual setting, use existing)<br>
Have yet to run pc2lib2.cli through the script and create password txt

Decided to scrap pc2_maker and fix the java gui already created