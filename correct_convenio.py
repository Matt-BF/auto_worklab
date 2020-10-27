import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

LABS = {
    # "ALP": "07",
    # "ANC": "03",
    # "BIC": "07",
    # "BIL": "07",
    # "CAE": "03",
    # "IBA": "03",
    # "DLT": "07",
    # "LAB": "05",
    # "LME": "07",
    # "LTE": "03",
    # "NAS": "03",
    # "REB": "04",
    # "DMS": "02",
    # "AND": "05",
    # "SM": "06",
    "CIT": "04",
    # "TRA": "07",
    # "MUE": "07",
}


def fix(code, cvn):
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
    driver.find_element_by_xpath(
        "/html/body/form/div/div[1]/div[3]/div[1]/div/a[2]"
    ).click()

    driver.find_element_by_xpath(
        '//*[@id="guidely-guide-1"]/div/div[2]/button'
    ).click()  # remover popup

    time.sleep(1)

    driver.find_element_by_xpath(
        "/html/body/form/div/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/table/thead[2]/tr/td[7]/select/option[2]"
    ).click()

    lab = driver.find_element_by_xpath('//*[@id="unidade"]')
    lab.send_keys(code)
    conv = driver.find_element_by_xpath('//*[@id="convenio"]')
    conv.send_keys(cnv)
    conv.send_keys(Keys.ENTER)

    num_patients = (
        driver.find_element_by_xpath('//*[@id="my-table_info"]')
        .text.split()[5]
        .replace(",", "")
    )
    for i in range(int(num_patients) + 1):  # loop for all patients
        if i != 0:
            driver.find_element_by_xpath(
                "/html/body/form/div/div/div[2]/div[2]/div[2]/div/div[1]/div[1]/div/table/thead[2]/tr/td[7]/select/option[2]"
            ).click()
            lab = driver.find_element_by_xpath('//*[@id="unidade"]')
            lab.send_keys(code)
            conv = driver.find_element_by_xpath('//*[@id="convenio"]')
            conv.send_keys(cnv)
            conv.send_keys(Keys.ENTER)

        ### try block for editing client (sometimes doesnt work) ###
        # if it doesnt work twice, check if table empty, if empty, go to next lab
        try:
            driver.find_element_by_xpath(
                "/html/body/form/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[7]/a[1]"
            ).click()
        except Exception:
            try:
                time.sleep(2)
                driver.find_element_by_xpath(
                    "/html/body/form/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[7]/a[1]"
                ).click()
            except Exception:
                if driver.find_element_by_class_name("dataTables_empty"):
                    driver.quit()
                    return "Finished"

        convenio = driver.find_element_by_id("tbConvenio")
        convenio.send_keys(Keys.CONTROL + "a")
        convenio.send_keys(Keys.DELETE)
        convenio.send_keys(code)
        convenio.send_keys(Keys.ENTER)

        driver.find_element_by_id("confirmapac").click()


for lab, cnv in LABS.items():
    fix(lab, cnv)
