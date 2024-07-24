# A More Detailed Documentation of Code Function

Currently, the python script uses OOP (Object-Oriented Programming) to create "pc2_instance" object. This object contains various functions that enable the user to complete necessary contest processes (i.e. opening PC2 account batch files) by piping batch output to the Python script. I recognize that this process is inefficient, and some may say that I might as well create a new PC2 library, but I am using Python at this point in time for the following reasons:

- To develop and apply my Python skills effectively
- To preserve the legacy of Hunter Han (Pure Java for this is insane)
- To have a working idea before I begin building software

## The Working Idea

The following list contains the functions within the "pc2_instance" object and their purpose, as well as creative work-arounds that may be important to identify.

### Constructor

**Feature:**

- Assign paths to instance variables that will be used in other functions.
- Change the working directory to the "bin" folder within the "pc2-9.8.0" contest folder.
- Create instance variables for subprocesses during opening of batch files in other functions.
- Create boolean instance variables to keep track of whether DHCP (Dynamic Host Configuration Protocol) has been disabled for WiFi and Ethernet.
- Create string instance variable to store the name of the ethernet service to be selected by the user in another function.

### get_help(self)

**Feature:**

- Print user instructions to terminal

### set_ini(self)

**Feature:**

- Calls function "get_ini_config" to check in "pc2v9.ini" exists and print the contest's current direct connection address configuration.
- Ask the user for the desired direct connection (localhost or an external IP address).
- Modify "pc2v9.ini" to match user's response with port 50002.

**Structures:**

- Uses a match-case structure in a while loop to ask for user input until the received input is valid. (This structure is used heavily throughout the script.)

### get_ini_config(self)

**Feature:**

- Check if "pc2v9.ini" exists in the expected path and stop the script if the file is not found.
- Print the current connection address.

### start_contest(self)

**Feature:**

- Create local variables to store string paths to the server and admin batch files.
- Call function "toggle_firewall" to change firewall settings (contest participants cannot directly connect to the server host if the host machine's firewall is not disabled).
- Call function "yn-command" process spawning with command prompt command to manually set static IP address "192.168.1.2" to host machine instead of DHCP.
- Open server batch file and read output upon successful login to open admin batch file.

**Structure:**

- When user has successfully logged into the server account, the server batch file output will contain the server profile that the user logged into. Using this profile output as an indication of successful login, the admin batch file is opened automatically for the user.

### run_other(self, other)

**Feature:**

- Uses an if statement to open an existing account batch file or print an error message if the batch file does not exist.

**Structure:**

- The "pc2" prefix is truncated from the user command and re-added in this function before the Popen process is spawned to provide simpler commands. Refer to the "pc2_runner.py" script.

### toggle_firewall(self)

**Feature:**

- Spawns process to store firewall display output text from NetSh command. From this stored text, the domain, private, and public firewall statuses are displayed to terminal for the user.
- Turn all firewall profiles on or off with NetSh command using input from user.

### yn_command(self, cmd)

**Feature:**

- Reusable function to ask user if the displayed command line command should be run.
- Implemented in other functions in the "pc2_instance" object.

### transfer_to_ethernet(self)

**Feature:**

- Instructs user to ensure that an ethernet connection has already been established.
- If user confirms contest transfer to ethernet connection, function "check_ether_connection" is called to begin ethernet selection process in command prompt and store the name of the selected ethernet connection.
- If the call to function "check_ether_connection" returns the message "exit", the ethernet swap process is exited. Otherwise, function "check_wifi_connection" is called to begin WiFi connection selection process and retrieve the properties of the selected WiFi network. Then the ethernet connection and the wifi connection are swapped, transferring the contest to the ethernet connection.
- The ethernet-wifi connections swap is a series of command line processes: (1) resetting the WiFi connection to DHCP, (2) disconnecting from the current WiFi connection, (3) connecting to the selected ethernet connection using the predefined static IP address, and (4) connecting to the selected WiFi connection.
- A swap confirmation message is displayed to terminal.

### check_ether_connection(self)

**Feature:**

- Pipe output from ipconfig command in a new command prompt process and populate an array of available ethernet connection names through a series of conditions and list operations.
- If the list of available ethernet connection names remains empty, an ethernet swap process exit message is displayed to terminal. Otherwise, a formatted display of the ethernet connections list is printed to terminal with each connection name corresponding to an indexed custom command and connection status (i.e. Media Disconnected).
- The user is given the option to select an ethernet connection among the formatted display by entering the custom command as displayed in the formatted display.
- Once a valid selection command has been entered, the user must confirm their selection ("y" or "n"). The function then returns the name of the selected ethernet connection to function "transfer_to_ethernet" if selection is confirmed. Otherwise, "exit" is returned to indicate that no connection is selected.

**Structure:**

- The formatted display of the available ethernet connections list is created and displayed line by line. The ethernet connection name is separated from the ethernet connection status by a string containing alternating periods and spaces. The number of digits in the ethernet connection's index in context of the ethernet connections list, the length of the ethernet connection name, and the length of the ethernet connection status are subtracted from a fixed length of 59 characters to determine the length of the separation string.
- All display values are concatenated at the end of the length calculations, and each concatenated line is printed sequentially.
- This structure is also implemented in function "check_wifi_connection".

### check_wifi_connection(self)

**Feature:**

- The function spawns a command line process to show current available WiFi connections and store piped output.
- For each line in the piped output, a series of conditions are evaluated in order to determine the properties of the current User-OS interface.
    - The adapter name is identified by determining if the line in the piped output contains the keyword "Name".
    - The current wireless network's SSID (service set identifier) is identified by determining if the line in the piped output contains the keyword "SSID".
    - A boolean local variable is used to track if the current line being evaluated falls under the "Primary" network category.
    - Another boolean local variable is used to confirm if the host machine is connected to the network under evaluation.
    
    If the two conditions "is_primary" and "is_cur_wifi" are met and the line contains the keyword "Profile", a tuple containing the identified adapter name, SSID, and profile name is stored in a local variable.
- The host device is disconnected from the current WiFi connection.
- A new command line process is spawned to retrieve the list of available networks and store the piped output.
- Each line in the output is checked for keywords "Interface" and "SSID" in order to identify the SSIDs of every available network and the names of the interfaces they fall under. The SSIDs and interface names are added to a dictionary, with the interfaces as the keys and sets of corresponding network SSIDs as the values.
- Displays the interface names stored in the dictionary and all the associated network SSIDs sequentially in a format: each interface name is followed by a formatted line for each network SSID (a custom command containing the network SSID index, followed by a spacer string, then the network SSID at the end). The lines are fixed at a length of 59 characters, so the spacer string length is calculated by subtracting the sum of the custom command length and the network SSID length.
- The user must select a network SSID using the corresponding custom command, and then respond to the confirmation question. If the user confirms the Wi-Fi connection process with "y", a tuple containing (1) the tuple with the original network properties (adapter name, SSID, and profile name) and (2) a new tuple containing the SSID of the selected WiFi network is returned to function "transfer_to_ethernet". If the user chooses to leave the confirmation process with "n", the message "exit" is returned.
- A process to reconnect to the original network is spawned.

### run_web_interface(self)

**Feature:**

- If the web team interface archive has been unzipped, the path to batch file "pc2wti.bat" will exist, and the batch file will be run by spawning a new process. Otherwise the web team interface zip file contents are extracted and the INI configuration file "pc2v9.ini" that exists as part of the web team interface package undergoes modifications to successfull start the web application.
- The user must input and confirm the desired scoreboard name and password.
- The INI configuration file is then rewritten line by line. The lines containing configurations for the web app scoreboard name and password are modified according to the user's previous scoreboard name and password input responses.
- In order to add a custom web team interface web application button for contest participants to download a sample data archive, a new "main.js" file must be created to replace the default JavaScript file, since the web app is built dynamically.
- The user is given the option of using the default "main.js" file or entering the path to the new "main.js" file. Similarly, if the assets folder is not found, the user is asked to enter the path to the new assets folder.