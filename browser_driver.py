import message
from selenium import webdriver


def get_driver(browser):
    if browser == 'chrome':
        '''
        Use Chrome - requires chromedriver in resources folder
        '''
        browser_options = webdriver.ChromeOptions()
        browser_options.add_argument("start-maximized")
        browser_options.add_argument("disable-infobars")
        browser_options.add_argument("--disable-extensions")
        browser_options.add_experimental_option('detach', True)  # keeps chrome and chromedriver open
        driver = webdriver.Chrome(
            executable_path=r'./resources/chromedriver89.0.4389.23.exe',
            options=browser_options
        )
    elif browser == 'firefox':
        '''
        Use Firefox - requires geckodriver  in resources folder
        '''
        browser_options = webdriver.FirefoxOptions()
        browser_options.add_argument("start-maximixed")
        browser_options.add_argument("disable-infobars")
        browser_options.add_argument("--disable-extensions")
        driver = webdriver.Firefox(executable_path=r'./resources/geckodriver.exe', options=browser_options)
    else:
        message.show_error('error: no browser selected')
        exit()

    return driver