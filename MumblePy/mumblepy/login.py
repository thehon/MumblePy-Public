from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
def loginUser(driver,username,password):
    try:
        driver.get('https://soundcloud.com/')
        sleep(8)

        #find the login button and click it
        loginButton = driver.find_element_by_class_name('frontHero__loginButton')
        ActionChains(driver).move_to_element(loginButton).click().perform()
        sleep(4)
        loginTextBox = driver.find_element_by_class_name('textfield__inputWrapper')
        #enter text in box
        ActionChains(driver).move_to_element(loginTextBox). \
                click().send_keys(username).perform()
        sleep(5)
        loginButton = driver.find_elements_by_class_name('signinForm__cta')
        #print("LOGIN BUTTON: ", loginButton)
        #loginButton[3] is the login we want
        ActionChains(driver).move_to_element(loginButton[3]).click().perform()

        sleep(5)
        #now we want to input the password and enter to login
        passwordField = driver.find_elements_by_xpath(
                "//input[@name='password']")

        ActionChains(driver).move_to_element(passwordField[0]). \
                click().send_keys(password).perform()

        ActionChains(driver).move_to_element(passwordField[0]). \
                click().send_keys(Keys.ENTER).perform()

        sleep(8)
        #make sure login was succesfull - check the username in the top corner
        return True
    except Exception as err:
        print('error logging in {}'.format(err))
        return False
