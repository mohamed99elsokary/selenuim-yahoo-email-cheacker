from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import glob
import threading
import colorama
from colorama import Fore
from getmac import get_mac_address as gma
colorama.init(autoreset=True)
mac = gma()
macs = ["d0:50:99:f9:fb:48"]
if mac in macs:

    path = "chromedriver.exe"
    url = "https://login.yahoo.com/account/challenge/session-expired?.intl=xa&intl=xa&.lang=ar-JO&src=ym&specId=yidreg&activity=header-signup&pspid=1197806870&done=https%3A%2F%2Fmail.yahoo.com%2Fd%3F.intl%3Dxa%26.lang%3Dar-JO%26.partner%3Dnone%26.src%3Dfp%26activity%3Duh-mail&authMechanism=secondary&acrumb=enokhtR8&lang=ar-JO"

    threads_number = int(input("how many threads do u want : "))


    def delete_old_emails():
        files = glob.glob("emails/*")
        for f in files:
            os.remove(f)


    delete_old_emails()

    with open("emails.txt") as f:
        emails = [line.rstrip() for line in f]


    def divide_emails_and_proxy():
        total = len(emails)
        if threads_number <= total:
            batchs = int(len(emails) / threads_number)
            for id, log in enumerate(emails):
                fileid = id / batchs
                file = open(
                    "emails/miniemails{file}.txt".format(
                        file=int(fileid) + 1
                    ),
                    "a+",
                )
                file.write(log + "\n")
        else:
            print(f"try to run it again but use a number lesser than {total+1}")
            exit()


    divide_emails_and_proxy()
    def cheack_rate_limte(email , all):
        if "rate limted" in all:
            print(f"{email} rate limted")
            exit()

    def check_email(file_number):
        with open(f"emails/miniemails{file_number}.txt") as f:
            emails = [line.rstrip() for line in f]
        for email in emails:
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

                print(f"{Fore.YELLOW}{email} is live")
                file = open(
                    "live emails.txt",
                    "a",
                )
                file.write(email)
                file.write("\n")

            driver.quit()


    threads = []
    for file_number in range(threads_number):
        file_number += 1
        file_number = str(file_number)

        thread1 = threading.Thread(target=check_email, args=(file_number,))
        thread1.start()
        threads.append(thread1)

    for thread2 in threads:
        thread2.join
else:
    print("your mac isn't known for us , bitch")
