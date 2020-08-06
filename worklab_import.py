import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd
import sys

def create_xml(csv, company):
    df = pd.read_csv(csv)
   # print(df.head())
    tree = ET.parse("template.xml")
    root = tree.getroot()
    today = datetime.today()

    # mexer no lote
    lote = root.find("Lote")
    cod_lote_lab = lote[1]
    data_lote = lote[2]
    cod_lote_lab.text = f"{datetime.strftime(today, '%Y%m%d')}_{company.split('.')[0]}"
    data_lote.text = datetime.strftime(today, "%Y-%m-%d")

    # adicionar pedido e pacientes
    for idx in df.index:
        pedido = ET.SubElement(lote, "Pedido")
        cod_ped = ET.SubElement(pedido, "CodPedLab")
        data_ped = ET.SubElement(pedido, "DataPed")
        cod_ped.text = str(idx+1)
        data_ped.text = f"{datetime.strftime(today,'%Y-%m-%d')}"

        paciente = ET.SubElement(pedido, "Paciente")
        # nome
        nome = ET.SubElement(paciente, "Nome")
        nome.text = df.loc[idx, "NOME"].strip().capitalize()
        # sexo
        sexo = ET.SubElement(paciente, "Sexo")
        sexo.text = df.loc[idx, "SEXO"].strip()
        # data nasc
        try:
            data_nasc = ET.SubElement(paciente, "DataNasc")
            data_nasc.text = datetime.strftime(datetime.strptime(
                df.loc[idx, "DATA_NASC"].strip(), "%d/%m/%Y"), "%Y-%m-%d")
        except AttributeError:
            pass

        for exam in df.loc[idx, "EXAMES"].split(" "):
            exame = ET.SubElement(pedido, "Exame")
            cod_exame = ET.SubElement(exame, "CodExmApoio")
            cod_exame.text = exam

    tree.write(sys.argv[1] + ".xml")


create_xml(sys.argv[1], sys.argv[1].split("."[0]))
