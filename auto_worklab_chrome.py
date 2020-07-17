import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys


def analyze_csv(plate_csv):
    df = pd.read_csv(plate_csv, skiprows=range(0, 19))
    df = df.set_index("Sample")
    df = df[["Well", "Target", "Cq"]]

    a = pd.pivot_table(df, values="Cq", index="Sample", columns="Target", dropna=False)

    # positive samples
    pos = a[(a["N1"] < 40) & (a["N2"] < 40)]
    pos.loc[:, "Result"] = "POSITIVO"

    # negative samples
    neg_null = a[(pd.isnull(a["N1"]) & (pd.isnull(a["N2"])) & (a["RP"] < 40))]
    neg_N1 = a[(a["N1"] > 40) & (pd.isnull(a["N2"])) & (a["RP"] < 40)]
    neg_N2 = a[(pd.isnull(a["N1"]) & (a["N2"] > 40) & (a["RP"] < 40))]
    neg_N1_N2 = a[(a["N1"] > 40) & (a["N2"] > 40) & (a["RP"] < 40)]
    neg = pd.concat([neg_null, neg_N1, neg_N2, neg_N1_N2])
    neg.loc[:, "Result"] = "NEGATIVO"

    # add inconclusive
    pos_neg = pd.concat([pos, neg])
    inc = a.loc[~a.index.isin(pos_neg.index)]
    inc.loc[:, "Result"] = "INCONCLUSIVO"

    consolidated = pd.concat([pos, neg, inc]).sort_values(by="Sample")

    return consolidated


def auto_laudo(result_table):
    INCONCLUSIVE = []

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

    # estou na tela home
    driver.find_element_by_xpath(
        "/html/body/form/div/div[1]/div[3]/div[2]/div/a[1]/img"
    ).click()  # tela de insercao de resultados

    # estou na tela de insercao de resultados
    for code in result_table.index:
        if result_table.loc[code, "Result"] != "INCONCLUSIVO" and code.isdigit():
            # abrir pagina do paciente pelo codigo
            codigo = driver.find_element_by_id("tbCodigoPaciente")  # celula de codigo
            # apagar o que tiver na celula e escrever o codigo
            codigo.send_keys(Keys.CONTROL + "a")
            codigo.send_keys(Keys.DELETE)
            codigo.send_keys(code)
            codigo.send_keys(Keys.ENTER)

            # hora de laudar
            driver.find_element_by_id("btExame1").click()  # botao do exame
            if result_table.loc[code, "Result"] == "POSITIVO":
                resultado = driver.find_element_by_id("tbResultado4492")
                resultado.send_keys(Keys.CONTROL + "a")
                resultado.send_keys(Keys.DELETE)
                resultado.send_keys("P")
                driver.find_element_by_id("btSalvar").click()
            else:
                driver.find_element_by_id("btSalvar").click()

        # salvar os inconclusivos para ver na mao
        else:
            INCONCLUSIVE.append(code)
    driver.quit()

    print(INCONCLUSIVE)


start = time.time()
auto_laudo(analyze_csv(sys.argv[1]))

print(f"Executado em {round(time.time()-start)} segundos")
