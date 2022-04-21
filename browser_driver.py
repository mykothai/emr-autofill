import message as msg
from selenium import webdriver


def get_driver(browser):
    try:
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
                executable_path=r'./resources/chromedriver100.0.4896.60.exe',
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
            msg.show_error('error: no browser selected')
            exit()

        return driver
    except Exception as e:
        msg.show_error(e)
