import smtplib, time
from selenium import webdriver
from twilio.rest import Client

# FILL OUT THESE FIELDS TO MATCH YOUR DATA
semester = "fall"
course_sched_num = "num"
class_num = "num"
eid = "eid"
eid_pass = "pass"

driver = webdriver.Chrome()
driver.get("https://utdirect.utexas.edu/apps/registrar/course_schedule/" + course_sched_num + "/" + class_num)
driver.maximize_window()

username = driver.find_element_by_name("IDToken1")
username.send_keys(eid)

password = driver.find_element_by_name("IDToken2")
password.send_keys(eid_pass)

driver.find_element_by_name("Login.Submit").click()

driver.refresh
driver.implicitly_wait(1)
status = driver.find_element_by_xpath("//table/tbody/tr/td[6]").text
class_name = driver.find_element_by_xpath("//section/h2").text
prof_name = driver.find_element_by_xpath("//table/tbody/tr/td[5]").text

def sendSMS():
    # REGISTER A TWILIO ACCOUNT AND GET AUTH IDS AND TOKENS
    account_sid = 'YOUR ID'
    auth_token = 'YOUR TOKEN'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body = class_name + ' with ' + prof_name + ' is ' + status + '!',
                        from_ = '+1 YOUR TWILIO NUMBER',
                        to = '+1 YOUR NUMBER'
                    )

open_status = "open"
open_reserved = "open; reserved"

while (status != open_status) & (status != open_reserved):
    driver.refresh
    driver.implicitly_wait(1)
    status = driver.find_element_by_xpath("//table/tbody/tr/td[6]").text
    print("not open")
    time.sleep(5)

sendSMS()
