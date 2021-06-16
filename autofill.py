import browser_driver
import extract_load_transform as elt
import message as msg
import time
import validate
import variables as var
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


def login(driver):
    print("Logging in")
    driver.find_element_by_xpath("//input[@id='login__input--username']").send_keys(var.user)
    driver.find_element_by_xpath("//input[@id='login__input--password']").send_keys(var.password)
    time.sleep(var.input_delay)
    driver.find_element_by_xpath("//button-primary[@id='login__input--submit']").click()


def add_patient(driver, last_name, first_name, dob, gender, phone):
    driver.find_element_by_xpath("//button-primary[@id='patient-search-dialog__button--add-new-patient']").click()

    msg.show_confirmation('Last name: ' + last_name)
    driver.find_element_by_xpath("//input[@Id='primary-info__input--last-name']").send_keys(last_name)

    msg.show_confirmation('First name: ' + first_name)
    driver.find_element_by_xpath("//input[@Id='primary-info__input--first-name']").send_keys(first_name)

    msg.show_confirmation('Gender: ' + gender)
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

        gender_select.send_keys(Keys.TAB)  # move to dob field
    except Exception as e:
        error_string = e, 'Specified gender not found!'
        msg.show_error(error_string)

    msg.show_confirmation('DOB: ' + dob)
    dob = dob.split('-')

    action_chain = ActionChains(driver)  # workaround for stale DOM
    action_chain.send_keys(dob[0]).send_keys(Keys.TAB).send_keys(dob[1]).send_keys(Keys.TAB).send_keys(dob[2])
    action_chain.perform()

    try:
        driver.find_element_by_xpath("//input[@data-placeholder='Home Phone']").send_keys(phone)  # 0 is default
    except Exception as e:
        error_string = e, 'Phone number not found!'
        msg.show_error(error_string)

    if var.env == 'dev':
        # workaround for invalid PHN to add patient in test env: check 'private' checkbox
        driver.find_element_by_xpath("//mat-checkbox[@Id='primary-info__checkbox--private']").click()

    msg.show_prompt("Check if patient information is correct. ")

    # click on footer div in case save button's not enabled
    driver.find_element_by_xpath("//div[@class='footer-container']").click()

    try:
        if driver.find_element_by_xpath("//form[@class='ng-untouched ng-dirty ng-valid']"):
            driver.find_element_by_xpath("//span[text()='SAVE']").click()
            print('Patient saved!')
    except Exception as e:
        error_string = e, 'Cannot SAVE, fields are missing or invalid'
        msg.show_error(error_string)

    try:
        if driver.find_element_by_xpath("//form[@class='ng-untouched ng-dirty ng-valid']"):
            driver.find_element_by_xpath("//span[text()='SAVE & CLOSE']").click()  # click save and close
            print('Patient information pop up saved and closed!')
    except Exception as e:
        error_string = e, 'Cannot SAVE & CLOSE, fields are missing or invalid'
        msg.show_error(error_string)


def add_billing(driver, service_date, fee_item, diag_code, md_number):
    msg.show_confirmation('Service date: ' + str(service_date))
    time.sleep(var.input_delay)
    msg.show_confirmation('MD number: ' + str(md_number))

    md_element = driver.find_element_by_xpath("//input[@data-placeholder='Ref. by MD Number']")
    md_element.clear()
    md_element.send_keys(md_number)  # enter md number

    time.sleep(var.input_delay)

    msg.show_confirmation('Fee item: ' + str(fee_item))
    fee_element = driver.find_element_by_xpath("//input[@data-placeholder='Fee Item']")
    fee_element.send_keys(fee_item)

    msg.show_confirmation('Diagnostic code: ' + str(diag_code))
    dc_element = driver.find_element_by_xpath("//input[@data-placeholder='Diagnostic Code']")
    dc_element.clear()
    dc_element.send_keys(diag_code)  # enter diagnostic code
    msg.show_prompt("Check if billing page is correct then continue. ")

    try:
        if driver.find_element_by_xpath("//form[@class='ng-star-inserted ng-dirty ng-touched ng-valid']"):
            driver.find_element_by_xpath("//span[text()='Create']").click()  # click save and close
            print('Patient information pop up saved and closed!')
    except Exception as e:
        error_string = e, 'Cannot CREATE, fields are missing or invalid'
        msg.show_error(error_string)


def main():
    start_time = time.time()
    try:
        validate.is_environment_set(var.env)
        df = elt.pandarize(var.env)
        driver = browser_driver.get_driver(var.browser)
        if var.env == 'dev':
            msg.dev_env_test()

        msg.show_prompt('Ready to start?')

        print('============================= ACCESSING WEBSITE ============================')
        driver.get(var.site)
        driver.implicitly_wait(3)
        login(driver)

        driver.find_element_by_xpath("//mat-icon[@id='tabs__icon--practitioner-dropdown']").click()

        if var.env == 'production':
            driver.find_element_by_xpath("//span[text()='Laksman, Z (ZLaksman)']").click()
        elif var.env == 'dev':
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

            print('============================= SEARCHING PATIENT BY PHN =====================')
            driver.find_element_by_xpath(
                "//button[@id='patient-selection-container__button--search-patient']").click()
            driver.find_element_by_xpath("//input[@id='patient-search-dialog__input--phn']").send_keys(phn)  # enter PHN

            is_patient_exist = False
            try:
                if driver.find_element_by_xpath("//div[@id='patient-search-dialog_label--no-patient-found']"):
                    print('No Patients Found...adding patient')
                    print('============================= ADDING NEW PATIENT =============================')
                    add_patient(driver, last_name, first_name, dob, gender, phone)

                    print('============================= BILLING INFORMATION =========================')
                    add_billing(driver, service_date, fee_item, diagnostic_code, md_number)
            except Exception as e:
                print(e)
                is_patient_exist = True
                pass

            if is_patient_exist:
                print('============================= PATIENT FOUND ================================')
                formatted_phn = phn[:4] + " " + phn[4:7] + " " + phn[7:]
                print("Patient found", formatted_phn)
                driver.find_element_by_xpath(
                    "//td[@class='mat-cell cdk-cell cdk-column-phn mat-column-phn ng-star-inserted']").click()

                add_billing(driver, service_date, fee_item, diagnostic_code, md_number)

            msg.show_success('\n============================= BILLING COMPLETE ============================\n')

            if var.env == 'dev':
                break  # prevent moving on to next row (patient)

        print("Done...closing driver")
    finally:
        msg.show_success("--- Elapsed time: %s minutes ---" % ((time.time() - start_time) / 60))


if __name__ == "__main__":
    main()
