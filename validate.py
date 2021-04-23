import message


def is_environment_set(env):
    if env not in ('dev', 'production'):
        message.show_error('Environment is not set...exiting program')
        exit()
    return True
