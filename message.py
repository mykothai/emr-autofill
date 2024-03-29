import variables as var
from termcolor import colored


def dev_env_test():
    print("'============================= Style Test ============================='")
    print(colored('Environment: \t' + var.env, 'yellow', attrs=['bold']))
    print(colored('Browser: \t' + var.browser, 'yellow', attrs=['bold']))
    print(colored('URL: \t' + var.site, 'yellow', attrs=['bold']))
    print(colored('USER INPUT color test', 'blue', attrs=['bold']))
    print(colored('ERROR color test', 'magenta', attrs=['bold']))
    print(colored("ELAPSED Time color test", 'white', 'on_green', attrs=['bold']))


def show_error(error_msg):
    print(colored(error_msg, 'red', attrs=['bold']))


def show_message(message):
    print(colored(message, 'blue', attrs=['bold']))


def show_confirmation(message):
    print(colored(message, 'yellow'))


def show_prompt(message, continue_prompt=True):
    while True:
        print(colored('\n' + message.upper() + " Continue? (y/n)" if continue_prompt else "", 'blue', attrs=['bold']))
        user_input = input()
        if user_input == 'y' or '0':
            break
        else:
            print(colored("Are you sure you want to QUIT the program? (y/n)", 'red'))
            terminate = input()
            if terminate == 'y' or '0':
                exit()


def show_success(message):
    print(colored(message, 'green', attrs=['bold']))


def show_info(message):
    print(colored(message, 'magenta'))
