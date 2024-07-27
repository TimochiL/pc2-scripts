import pc2_instance as pc2

def main():
    pc2i = pc2.pc2_instance()
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
                print("'pc2_runner.py' terminated by user.")
            case "/ethernet":
                pc2i.transfer_to_ethernet()
            case "/wti":
                pc2i.run_web_interface()
            case "/set wti":
                pc2i.modify_web_interface()
            case "/set ini":
                pc2i.set_ini()
            case "/h":
                pc2i.get_help()
            case default:
                pc2i.run_other(command)
                    
if __name__ == '__main__':
    try:
        main()
    except Exception as ex:
        errorTypeTemplate = "\tException {0} occurred"
        errorArgsTemplate = "\t{0}"
        errorTypeMessage = errorTypeTemplate.format(type(ex).__name__)
        if len(ex.args) > 1:
            errorArgsMessage = errorArgsTemplate.format(ex.args[1])
        else:
            errorArgsMessage = errorArgsTemplate.format("Contest process terminated unexpectedly")
        
        errorCharacterWidth = max(len(errorTypeMessage), len(errorArgsMessage)) + 16 # Width of tab is 8 characters
        errorSeparatorLine = ''.join(['-']*errorCharacterWidth)
        
        print()
        print(errorSeparatorLine, errorTypeMessage, errorArgsMessage, errorSeparatorLine, sep='\n\n')
