# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.3] - 2024-07-26

### Added

- Command to modify Web Interface and UI apart from after unzipping WTI zip archive

### Changed

- More specific and easier to read error messages
- Modifications to Web Interface batch file and UI occur in function "modify_web_interface"
- DOCS.md to reflect function modifications
- Script help message

### Fixed

- Incorrect path to pc2wti.bat after unzip
- Working path and zip path hell
- Cannot access Web Team Interface .jar file (working directory must be parent folder of bin)

## [1.0.2] - 2024-07-24

### Added

- Custom Web Team Interface assets zip archive unzip functionality
- Better error handling

### Fixed

- pc2_instance Instantiation error
- instance.started does not exist
- Web Team Interface web app replace main.js and assets folder functionality 

## [1.0.1] - 2024-07-23

### Added

- "pc2_instance.py" contains the core module of the script (the pc2_instance object)
- "DOCS.md" to explain the ideas behind the script and programming decsions
- method "run_web_interface" to provide automated unzip and runnign of web UI package functionality

### Changed

- "pc2_runner.py" now contains only the main method
- "README.md" to include information about deprecated features

## [1.0.0] - 2023-11-18

### Changed

- Running the script changed to allow user to pass contest path argument through command line

## [Unreleased]

## [0.0.5] - 2023-04-14

### Added

- Wifi reconnection option after connecting to ethernet

### Fixed

- Ethernet not connecting due to attempt to connect to same network as Wireless LAN

## [0.0.4] - 2023-03-25

### Added

- Implement feature to change server setting on pc2v9.ini
- Add "CHANGELOG.md"

### Fixed

- Fix ethernet selection command reading bug.

### Changed

- Change "README.md" to serve its intended purpose.

## [0.0.3] - 2023-03-24

### Added

- Implement transfer to contest ethernet ability.

### Fixed

- Fix ethernet transfer bugs.

## [0.0.2] - 2023-03-18

### Added

- Consideration of get_pass function implementation for getting the password of a user entered team number.

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

- Added pc2_maker.py

### Changed

- Update help message to account for existing features of the runner.
- Put "pc2_maker.py" on hold for production

## [0.0.1] - 2023-03-17

### Added

- First version of pc2_runner.py with pc2 automation of internet and firewall config and contest startup.

[unreleased]: https://github.com/TimochiL/pc2-scripts/compare/1.0.3...HEAD
[1.0.3]: https://github.com/TimochiL/pc2-scripts/compare/1.0.2...1.0.3
[1.0.2]: https://github.com/TimochiL/pc2-scripts/compare/1.0.1...1.0.2
[1.0.1]: https://github.com/TimochiL/pc2-scripts/tree/1.0.1
