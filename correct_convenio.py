import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

LABS = [
    {"login": "875nasa", "password": "n454l48", "convenio_code": "03"},
]

for lab_dict in LABS:
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

    user_box.send_keys(lab_dict["login"])
    pass_box.send_keys(lab_dict["password"])
    submit.click()

    # tela home
    driver.find_element_by_xpath(
        "/html/body/form/div/div[1]/div[3]/div[1]/div/a[2]"
    ).click()

    convenio = driver.find_element_by_xpath("//*[@id="convenio"]")
    convenio.send_keys("01")

