import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

LABS = {
    "2": ("NAS", "03"),
    "3": ("CM", "03"),
    "4": ("IBA", "03"),
    "5": ("ANC", "03"),
    "6": ("LTE", "03"),
    "9": ("ANA", "04"),
    "10": ("CAE", "03"),
    "11": ("LAB", "05"),
    "12": ("DMS", "02"),
    "15": ("REB", "04"),
    "17": ("AND", "05"),
    "18": ("SM", "06"),
    "19": ("CIT", "04"),
}


for code, tup in LABS.items():
    driver = webdriver.Chrome(executable_path="./chromedriver")
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

    # tela home
    # trocar unidade
    driver.find_element_by_xpath(
        f"/html/body/form/div/div[1]/div[1]/div/div[2]/select/option[{code}]"
    ).click()

    time.sleep(1)
    driver.switch_to.alert.accept()

    driver.find_element_by_xpath(
        "/html/body/form/div/div[1]/div[3]/div[1]/div/a[2]"
    ).click()

    time.sleep(3)

    lab = driver.find_element_by_xpath('//*[@id="unidade"]')
    lab.send_keys(tup[0])
    lab.send_keys(Keys.ENTER)

    num_patients = (
        driver.find_element_by_xpath('//*[@id="my-table_info"]')
        .text.split()[5]
        .replace(",", "")
    )
    for i in range(int(num_patients) + 1):  # loop for all patients
        if i != 0:
            lab = driver.find_element_by_xpath('//*[@id="unidade"]')
            lab.send_keys(tup[0])
        convenio = driver.find_element_by_xpath('//*[@id="convenio"]')
        convenio.send_keys("01")
        convenio.send_keys(Keys.ENTER)
        time.sleep(1)
        driver.find_element_by_xpath(
            "/html/body/form/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[7]/a[1]"
        ).click()
        convenio = driver.find_element_by_id("tbConvenio")
        convenio.send_keys(Keys.CONTROL + "a")
        convenio.send_keys(Keys.DELETE)
        convenio.send_keys(tup[1])
        convenio.send_keys(Keys.ENTER)

        driver.find_element_by_id("confirmapac").click()

    driver.quit()
