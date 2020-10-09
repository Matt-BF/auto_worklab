import PyPDF2
import sys
import pandas as pd
from datetime import datetime


def parse_laudos(pdf):
    ALL_PATIENTS = []
    with open(pdf, "rb") as f:
        pdfReader = PyPDF2.PdfFileReader(f)

        for pageNum in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)
            text = pageObj.extractText().split("\n")
            info_dict = {
                "Protocolo": text[9],
                "Nome": text[7],
                "Idade": text[11],
                "Sexo": text[13],
                "Medico": text[20],
                "Data de Cadastro": text[15],
                "Data de Emissao do Resultado": text[18],
                "Resultado": text[35],
            }
            if "ELISA" in text:
                info_dict["Tipo de exame"] = "ELISA"
            elif "RT-qPCR" in text:
                info_dict["Tipo de exame"] = "RT-qPCR"

            ALL_PATIENTS.append(info_dict)

    return ALL_PATIENTS


def make_csv(patients_info):
    date_time = "_".join(str(datetime.now()).split())
    table = pd.concat([pd.DataFrame([i]) for i in patients_info], ignore_index=True)
    return table.to_csv(f"{date_time}_Dados_notificacao.csv", index=None)


if __name__ == "__main__":
    make_csv(parse_laudos(sys.argv[1]))
