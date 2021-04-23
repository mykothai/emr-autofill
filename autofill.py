from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from colorama import init
from termcolor import colored
from sys import exit
from tkinter import filedialog

# Set up
load_dotenv()
site = os.environ.get('SITE')
browser = os.environ.get('BROWSER')
env = os.environ.get('ENV')
if env == 'production':
    user = os.environ.get('USER')
    password = os.environ.get('PASSWORD')
else:
    user = os.environ.get('TEST_USER')
    password = os.environ.get('TEST_PASSWORD')
time_between_input = 0.5


def init_colorama():
    return init()


def dev_env_test():
    print(colored('Environment: \t' + env, 'yellow', attrs=['bold']))
    print(colored('Browser: \t' + browser, 'yellow', attrs=['bold']))
    print(colored('URL: \t' + site, 'yellow', attrs=['bold']))
    print(colored('USER INPUT color test', 'blue', attrs=['bold']))
    print(colored('ERROR color test', 'magenta', attrs=['bold']))
    print(colored("ELAPSED Time color test", 'white', 'on_green', attrs=['bold']))


def read_csv(file):
    try:
        return pd.read_csv(file)
    except Exception as e:
        show_error('Unable to read file ERROR: ' + str(e))


def to_datetime(date):
    return date.to_datetime()


def elt_data(env):
    print('============================= VALIDATING DATA =============================')
    # Do the data things
    print('Read CSV file...')
    if env == 'production':
        df = read_csv('E:/auto-form-fill/data.csv')
    elif env == 'dev':
        df = read_csv('E:/auto-form-fill/test_data.csv')
    df[' PHN'] = df[' PHN'].astype('str')  # field
    df[' DOB'] = pd.to_datetime(df[' DOB'], format='%d/%m/%Y').astype(str)  # format is the existing data format
    df[' Interpretation Date'] = pd.to_datetime(df[' Interpretation Date'], format='%d/%m/%Y').astype(
        str)  # format is the existing data format
    df[' Ref Doctor BillTo #'] = df[' Ref Doctor BillTo #'].apply(
        lambda x: '{0:0>5}'.format(x))  # add leading zeros to get 5 digits

    return df


def login(driver):
    print("Logging in")
    driver.find_element_by_xpath("//input[@id='login__input--username']").send_keys(user)
    driver.find_element_by_xpath("//input[@id='login__input--password']").send_keys(password)
    time.sleep(time_between_input)
    driver.find_element_by_xpath("//button-primary[@id='login__input--submit']").click()


def user_prompt(message):
    print(colored('\n' + message.upper() + " Continue? (y/n)", 'blue', attrs=['bold']))
    user_input = input()
    if user_input == 'y':
        pass
    else:
        print(colored("Are you sure you want to QUIT the program? (y/n)", 'red'))
        terminate = input()
        if terminate == 'y':
            exit()
        else:
            pass


def send_delayed_keys(element, text, delay=0.2):
    for character in text:
        end_time = time.time() + delay
        element.send_keys(character)
        time.sleep(end_time - time.time())


def select_browser(browser):
    if browser == 'chrome':
        '''
        Use Chrome - requires chromedriver in resources folder
        '''
        # set optional browser options
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
        show_error('error: no browser selected')
        exit()

    return driver


def is_environment_set(env):
    if env not in ('dev', 'production'):
        show_error('Environment is not set...exiting program')
        exit()
    return True


def show_error(error_msg):
    print(colored(error_msg, 'magenta', attrs=['bold']))


def add_patient(driver, last_name, first_name, dob, gender, phone):
    driver.find_element_by_xpath("//button-primary[@id='patient-search-dialog__button--add-new-patient']").click()

    print(colored('Last name: ' + last_name, 'yellow'))
    driver.find_element_by_xpath("//input[@Id='primary-info__input--last-name']").send_keys(last_name)

    print(colored('First name: ' + first_name, 'yellow'))
    driver.find_element_by_xpath("//input[@Id='primary-info__input--first-name']").send_keys(first_name)

    print(colored('DOB: ' + dob, 'yellow'))  # TODO date entry bug: sometimes too fast
    dob_input = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((
            By.XPATH, "//div[@class='input-row red-border']")))

    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((
            By.XPATH, "//div[@class='input-row red-border']"))).click()
    time.sleep(time_between_input)

    action_chain = ActionChains(driver)  # workaround for stale DOM
    action_chain.move_to_element(dob_input).send_keys(dob).perform()  # enters DOB

    print(colored('Gender: ' + gender, 'yellow'))
    try:
        gender_select = driver.find_element_by_xpath("//mat-select[@Id='primary-info__select--gender']")
        action_chain = ActionChains(driver)  # workaround for stale DOM
        action_chain.move_to_element(gender_select).click().perform()

        if gender == 'M':
            driver.find_element_by_xpath("//mat-option[@value='M']").click()
        elif gender == 'F':
            driver.find_element_by_xpath("//mat-option[@value='F']").click()
        elif gender == 'T':
            driver.find_element_by_xpath("//mat-option[@value='T']").click()
    except Exception as e:
        error_string = e, 'Specified gender not found!'
        show_error(error_string)

    driver.find_element_by_xpath("//input[@placeholder='Home Phone']").send_keys(
        phone)  # set phone number to 0 (default)

    if env == 'dev':
        # workaround for invalid PHN to add patient: check 'private' checkbox [testing]
        driver.find_element_by_xpath("//mat-checkbox[@Id='primary-info__checkbox--private']").click()

    user_prompt("Check if patient information is correct. ")

    # click on footer div in case save buttons not enabled
    driver.find_element_by_xpath("//div[@class='footer-container']").click()

    try:  # TODO except block never executed (suspect save button always available)
        if driver.find_element_by_xpath("//form[@class='ng-untouched ng-dirty ng-valid']"):
            driver.find_element_by_xpath("//span[text()='SAVE']").click()
            print('Patient saved!')
    except Exception as e:
        error_string = e, 'Cannot SAVE, fields are missing or invalid'
        show_error(error_string)

    # try:
    #     if not driver.find_element_by_xpath("//div[text()='Please save patient first']"):
    #         driver.find_element_by_xpath("//span[text()=' MSP CHECKED ']").click()  # click check msp
    #         print('MSP CHECKED button clicked')
    # except Exception as e:
    #     print(e, 'Cannot CHECK MSP, fields are missing or invalid')

    try:
        if driver.find_element_by_xpath("//form[@class='ng-untouched ng-dirty ng-valid']"):
            driver.find_element_by_xpath("//span[text()='SAVE & CLOSE']").click()  # click save and close
            print('Patient information pop up saved and closed!')
    except Exception as e:
        error_string = e, 'Cannot SAVE & CLOSE, fields are missing or invalid'
        show_error(error_string)


def add_billing(driver, service_date, fee_item, diag_code, md_number):
    print(colored('Service date: ' + str(service_date), 'yellow'))

    # TODO for now, manually enter service date
    # user_prompt("Input service date then continue. ")
    # print('service date ', patient[12])
    # service_date_input = driver.find_element_by_xpath("//div[@class='input-row red-border']")
    # WebDriverWait(driver, 5).until(
    #     EC.element_to_be_clickable((
    #         By.XPATH, "//div[@class='input-row red-border']"))).click()
    # action.move_to_element(service_date_input).send_keys(service_date).perform()  # enter service date

    time.sleep(time_between_input)

    print(colored('MD number: ' + str(md_number), 'yellow'))
    md_element = driver.find_element_by_xpath("//input[@placeholder='Ref. by MD Number']")
    md_element.clear()
    md_element.send_keys(md_number)  # enter md number

    time.sleep(time_between_input)

    print(colored('Fee item: ' + str(fee_item), 'yellow'))
    # driver.find_element_by_xpath("//input[@placeholder='Fee Item']").send_keys(fee_item)  # enter fee item
    fee_element = driver.find_element_by_xpath("//input[@placeholder='Fee Item']")
    send_delayed_keys(fee_element, str(fee_item))

    fee_element.send_keys(Keys.BACKSPACE)  # removes existing input
    time.sleep(time_between_input)
    send_delayed_keys(fee_element, str(fee_item)[-1:])

    print(colored('Diagnostic code: ' + str(diag_code), 'yellow'))
    dc_element = driver.find_element_by_xpath("//input[@placeholder='Diagnostic Code']")
    dc_element.clear()
    dc_element.send_keys(diag_code)  # enter diagnostic code

    # TODO commented out error message: not right way to handle doctor not found
    # try:
    #     if driver.find_element_by_xpath("//mat-hint[@text=' Failed to load doctor ']"):
    #         # user_prompt("Please add new doctor, then continue.")
    #
    #         # TODO complete add new doctor form
    #         '''
    #         if doctor DNE:
    #             (driver.find_element_by_xpath("//mat-hint[text()=' Failed to load doctor ']")
    #             click on magnifying glass
    #                 click add new > MSP, last name, first name, phone = 0
    #         '''
    #         driver.find_element_by_xpath(
    #             "//mat-icon[@class='mat-icon notranslate new-search-prefix mat-icon-no-color ng-tns-c120-104']"
    #         ).click()
    #         driver.find_element_by_xpath("//button-secondary[@id='doctor-search-dialog__button--add']").click()
    #         # TODO function to parse doctor name from patient[8]
    # except Exception as e:
    #     show_error(e)
    #     pass

    user_prompt("Check if billing page is correct then continue. ")

    try:
        if driver.find_element_by_xpath("//form[@class='ng-star-inserted ng-dirty ng-touched ng-valid']"):
            driver.find_element_by_xpath("//span[text()='Create']").click()  # click save and close
            print('Patient information pop up saved and closed!')
    except Exception as e:
        error_string = e, 'Cannot CREATE, fields are missing or invalid'
        show_error(error_string)


def main():
    is_environment_set(env)
    init_colorama()
    start_time = time.time()
    df = elt_data(env)
    driver = select_browser(browser)
    if env == 'dev':
        dev_env_test()

    user_prompt('Ready to start?')

    print('============================= ACCESS WEBSITE ==============================')
    print('Open EMR')
    driver.get(site)
    driver.implicitly_wait(3)  # driver waits before searching when element is not present
    login(driver)

    driver.find_element_by_xpath("//mat-icon[@id='tabs__icon--practitioner-dropdown']").click()

    if env == 'production':
        driver.find_element_by_xpath("//span[text()='Laksman, Z (ZLaksman)']").click()
    elif env == 'dev':
        driver.find_element_by_xpath("//span[text()='MD, S (S-MD)']").click()

    driver.find_element_by_xpath("//button[@id='sidebar-component__button--app-selector-button']").click()
    driver.find_element_by_xpath("//span[text()='Billing']").click()

    print("Start data entry")
    for patient in df.itertuples():
        phn = patient[3]
        last_name = patient[4]
        first_name = patient[5]
        dob = patient[7]
        gender = patient[6]
        phone = 0
        md_number = patient[10]
        service_date = patient[12]
        fee_item = patient[13]
        diagnostic_code = patient[14]

        print('============================= SEARCH PATIENT BY PHN =======================')
        driver.find_element_by_xpath("//mat-icon[@id='patient-selection-container__button--search-patient']").click()
        driver.find_element_by_xpath("//input[@id='patient-search-dialog__input--phn']").send_keys(phn)  # enter PHN

        is_patient_exist = False
        try:
            if driver.find_element_by_xpath("//div[@id='patient-search-dialog_label--no-patient-found']"):
                print('No Patients Found...adding patient')
                print('============================= ADD NEW PATIENT =============================')
                add_patient(driver, last_name, first_name, dob, gender, phone)

                print('============================= BILLING INFORMATION =========================')
                add_billing(driver, service_date, fee_item, diagnostic_code, md_number)
        except Exception as e:
            print(e)
            is_patient_exist = True
            pass

        if is_patient_exist:
            print('============================= PATIENT FOUND ===============================')
            formatted_phn = phn[:4] + " " + phn[4:7] + " " + phn[7:]
            print("Patient found", formatted_phn)
            driver.find_element_by_xpath(
                "//td[@class='mat-cell cdk-cell cdk-column-phn mat-column-phn ng-star-inserted']").click()

            add_billing(driver, service_date, fee_item, diagnostic_code, md_number)

        print(colored('\n============================= BILLING COMPLETE ============================\n', 'white', 'on_green'))

        if env == 'dev':
            break  # prevent moving on to next row (patient)

    print("Done...closing driver")
    # driver.close()  # closes browser
    print(colored("--- Elapsed time: %s minutes ---" % ((time.time() - start_time) / 60),
                  'white',
                  'on_green',
                  attrs=['bold']
                  )
          )


if __name__ == "__main__":
    main()
