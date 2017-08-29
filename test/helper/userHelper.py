import time
import pdb
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common,desired_capabilities import DesiredCapabilities
from config import env

class UserHelper():

    driver = None

    @classmethod
    def startDriver(cls):
        cls.driver = webdriver.Remote("http://0.0.0.0:4444/wd/hub", DesiredCapabilities.CHROME)
        cls.driver.implicitly_wait(60)
        cls.driver.set_window_size(1280, 1080)

    @classmethod
    def stopDriver(cls):
        cls.driver.close()

    @staticmethod
    def find_elem(selector, name=False):
        if name == True:
            return UserHelper.driver.find_element_by_name(selector)
        elif selector[0:2] == '//':
            return UserHelper.driver.find_element_by_xpath(selector)
        else:
            return UserHelper.driver.find_element_by_css_selector(selector)

    @staticmethod
    def setInput(selector, value, name=False):
        elem = UserHelper.find_elem(selector, name)
        elem.send_keys(value)

    @staticmethod
    def click(selector, name=False, xpath=False):
        if name == True:
            elem = WebDriverWait(UserHelper.driver, 20).until(EC.element_to_be_clickable((By.NAME, selector)))
        elif xpath == True:
            elem = WebDriverWait(UserHelper.driver, 20).until(EC.element_to_be_clickable((By.XPATH, selector)))
        else:
            elem = WebDriverWait(UserHelper.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))

        time.sleep(1)
        elem.click()

    @staticmethod
    def wait_visible(locator):
        WebDriverWait(UserHelper.driver, 20).until(EC.visibility_of_element_located(locator))

    @staticmethod
    def wait_invisible(locator):
        WebDriverWait(UserHelper.driver, 20).until(EC.invisibility_of_element_located(locator))

    @staticmethod
    def login_okta(user):
        print('===========login through okta============')
        driver = UserHelper.driver

        driver.get(env["okta"]["url"])
        UserHelper.setInput("username", user["username"], name=True)
        UserHelper.setInput("password", user["password"], name=True)
        UserHelper.click(".button")
        time.sleep(5)
        UserHelper.setInput('answer', user["twoStep"], name=True)
        UserHelper.click("input.button")
        UserHelper.find_elem('//*[@id="container"]/div/div[2]/div/div[2]/ul[2]/li[2]/a')
        driver.get(env["okta"]["jiveSSOLoginUrl"])
        time.sleep(15)

    @staticmethod
    def login_jive(user):
        driver = UserHelper.driver

        driver.get(env["jive"]["url"])
        UserHelper.setInput("username", user["username"], name=True)
        UserHelper.setInput("password", user["password"], name=True)
        UserHelper.click("#login-submit")
        time.sleep(15)

    @staticmethod
    def login(user):
        if env["loginMethod"] == "jive":
            UserHelper.login_jive(user)
        elif env["loginMethod"] == "okta":
            UserHelper.login_okta(user)


    @staticmethod
    def createGroup(groupName):
        UserHelper.driver.get(env["jive"]["url"])
        UserHelper.click('#navCreate')
        UserHelper.click('#create-list-2 > li > a')

        UserHelper.driver.switch_to.frame(UserHelper.driver.find_element_by_name('__gadget_j-app-modal-parent'))

        UserHelper.setInput("#groupname", groupName)
        UserHelper.setInput("#description", "This group is use for test create group")
        UserHelper.click('#jive-socialgroup-type-PRIVATE')
        UserHelper.click('#ext_invites_checkbox')

        UserHelper.click("#submit-group")
        UserHelper.driver.switch_to.default_content()

        time.sleep(50)

        if UserHelper.driver.current_url != env['jive']['url'] + 'groups/' + groupName:
            raise Exception('Create Group Failed! not jumped to group url')

    @staticmethod
    def addMembersToGroup(groupName, members):
        UserHelper.driver.get(env["jive"]["url"]+"groups/"+groupName)
        UserHelper.click('#jive-place-link-actions')
        UserHelper.click('#j-place-actions-container [data-label="Manage Users"]')

        UserHelper.driver.switch_to.frame(UserHelper.driver.find_element_by_name('__gadget_j-app-modal-parent'))

        UserHelper.wait_visible((By.CSS_SELECTOR, "#spinner"))
        UserHelper.wait_invisible((By.CSS_SELECTOR, "#spinner"))

        for member in members:
            UserHelper.setInput('#add-twer input[type="text"]', member['username'])
            UserHelper.wait_visible((By.CSS_SELECTOR, '#add-twer .selectize-dropdown .selectize-dropdown-content'))
            time.sleep(1)
            UserHelper.click('#add-twer .selectize-dropdown-content [data-value="'+member["email"]+'"]')


        UserHelper.click('#submit-users')
        UserHelper.driver.switch_to.default_content()
        time.sleep(60)
