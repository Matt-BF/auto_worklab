from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys


def laudos_codigo(code_file):
    with open(code_file) as f:
        codes = [line.strip() for line in f]
    driver = webdriver.Firefox(executable_path="./geckodriver")
    driver.get("https://app.worklabweb.com.br/index.php")

    # estou na tela de login
    user_box = driver.find_element_by_xpath(
        "/html/body/div/div/div[2]/div[1]/form/div[3]/div[1]/input"
    )  # user
    pass_box = driver.find_element_by_xpath(
        "/html/body/div/div/div[2]/div[1]/form/div[3]/div[2]/input"
    )  # pass
    submit = driver.find_element_by_xpath(
        "/html/body/div/div/div[2]/div[1]/form/div[5]/button"
    )

    user_box.send_keys("875bruna")
    pass_box.send_keys("bruninha1234")
    submit.click()

    # estou na tela home
    driver.find_element_by_xpath(
        "/html/body/div/div/div[2]/ul/li[1]/div[2]/ul[4]/li[6]/a"
    ).click()  # link do laudos por codigo

    # estou na tela de laudos por codigo
    driver.quit()


laudos_codigo(sys.argv[1])
