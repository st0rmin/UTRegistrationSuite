import smtplib, time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from twilio.rest import Client

semester = "fall"
course_sched_num = "num"
class_num = "num"
drop_class_num = "num"
eid = "eid"
eid_pass = "pass"
drop = True
repeat = True

driver = webdriver.Chrome()
driver.get("https://utdirect.utexas.edu/apps/registrar/course_schedule/" + course_sched_num + "/" + class_num)
driver.maximize_window()

username = driver.find_element_by_name("IDToken1")
username.send_keys(eid)

password = driver.find_element_by_name("IDToken2")
password.send_keys(eid_pass)

driver.find_element_by_name("Login.Submit").click()

driver.refresh()
driver.implicitly_wait(1)
status = driver.find_element_by_xpath("//table/tbody/tr/td[6]").text
class_name = driver.find_element_by_xpath("//section/h2").text
prof_name = driver.find_element_by_xpath("//table/tbody/tr/td[5]").text

def sendSMS(errors):
    # REGISTER A TWILIO ACCOUNT AND GET AUTH IDS AND TOKENS
    account_sid = 'YOUR ID'
    auth_token = 'YOUR TOKEN'
    client = Client(account_sid, auth_token)

    if not errors :
        message = client.messages \
                    .create(
                        body = class_name + ' with ' + prof_name + ' is ' + status + '! It has been added to your schedule. ' 
                            + 'Double check registration to make sure everything went smoothly.',
                        from_ = '+1 YOUR TWILIO NUMBER',
                        to = '+1 YOUR NUMBER'
                    )
    else :
        message = client.messages \
                    .create(
                        body = class_name + ' with ' + prof_name + ' is ' + status + ', but you could not be registered.',
                        from_ = '+1 YOUR TWILIO NUMBER',
                        to = '+1 YOUR NUMBER'
                    )

def navigateToRegistration():
    driver.get("https://utdirect.utexas.edu/registration/chooseSemester.WBX")
    register_semester_options = driver.find_elements_by_name("submit")
    button = register_semester_options[1]
    if (semester == "summer"):
        button = register_semester_options[0]
    else :
        button = register_semester_options[1]

    button.click()

    registerClass()

def registerClass():

    driver.refresh()
    driver.implicitly_wait(1)
    if drop :
        select_button = driver.find_elements_by_name("s_request")[2]
        select_button.click()
        select_class_dropdown = Select (driver.find_element_by_name("s_swap_unique_drop"))
        select_class_dropdown.select_by_value(drop_class_num)
        class_entry = driver.find_element_by_name("s_swap_unique_add")
        class_entry.send_keys(class_num)
    else :
        class_entry = driver.find_element_by_name("s_unique_add")
        class_entry.send_keys(class_num)

    driver.find_element_by_name("s_submit").click()
    errors = driver.find_elements_by_class_name("error")

    if not repeat :
        sendSMS(errors)
    elif errors :
        time.sleep(5)
        print("can't register")
        navigateToRegistration()

    sendSMS(errors)

open_status = "open"
open_reserved = "open; reserved"

while (status != open_status) & (status != open_reserved):
    driver.refresh()
    driver.implicitly_wait(1)
    status = driver.find_element_by_xpath("//table/tbody/tr/td[6]").text
    print("not open")
    time.sleep(5)

navigateToRegistration()
