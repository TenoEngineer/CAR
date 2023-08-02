import os
from datetime import date

import pandas as pd
from bs4 import BeautifulSoup
from requests_html import HTMLSession

USER_PATH = os.path.expanduser("~")
PROJECT_PATH = "\OneDrive\Power BI\CAR"
# ABSOLUT_PATH = os.path.join(USER_PATH, PROJECT_PATH, "\cars.xlsx")
# i don't know why join didn't work
ABSOLUT_PATH = USER_PATH + PROJECT_PATH + "\cars.xlsx"

session = HTMLSession()
today = date.today()

link_face = "https://www.facebook.com/marketplace/109764205717440/carros?minPrice=9000&maxPrice=13000&exact=false"
link_olx = "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-rs?pe=13000&ps=9000"
data = {
    "Price": [],
    "Title": [],
    "Region": [],
    "Km": [],
    "Year": [],
    "Date": [],
    "Link": [],
    "Description": [],
    "CEP": [],
    "City": [],
    "Model": [],
    "Type Car": [],
    "Power": [],
    "Color": [],
    "Doors": [],
    "Steering": [],
    "Optional": [],
}

links_olx = []


def olx_descriptions(url):
    r = session.get(url)
    try:
        cep = r.html.find(".ad__sc-1f2ug0x-1.cpGpXB.sc-hSdWYo.gwYTWo")[0].text
    except IndexError:
        cep = None
    try:
        cidade = r.html.find(".ad__sc-1f2ug0x-1.cpGpXB.sc-hSdWYo.gwYTWo")[1].text
    except IndexError:
        cidade = None
    try:
        description = r.html.find(".ad__sc-1sj3nln-1.fMgwdS.sc-hSdWYo.htqcWR")[0].text
    except IndexError:
        description = None
    list_description = r.html.find(".sc-kafWEX.jucPQk")
    dict_description = {}
    for i in list_description:
        key = i.find("span")[0].text
        try:
            value = i.find("a")[0].text
        except IndexError:
            value = i.find("span")[1].text

        dict_description[key] = value

    try:
        type_car = dict_description['Tipo de veículo']
    except KeyError:
        type_car = None
    try:
        power = dict_description['Potência do motor']
    except KeyError:
        power = None
    try:
        color = dict_description['Cor']
    except KeyError:
        color = None
    try:
        doors = dict_description['Portas']
    except KeyError:
        doors = None
    try:
        steering = dict_description['Tipo de direção']
    except KeyError:
        steering = None
    try:
        complet_model = dict_description['Modelo']
    except KeyError:
        complet_model = None
    price = r.html.find(".ad__sc-1leoitd-0.bJHaGt.sc-hSdWYo.dDGSHH")[0].text
    optional_all = []
    for i in r.html.find(".sc-bwzfXH.ad__h3us20-0.cyymIl"):
        optional_all.append(i.text)
    return (
        description,
        cep,
        cidade,
        complet_model,
        type_car,
        power,
        color,
        doors,
        steering,
        ";".join(optional_all),
        price
    )


olx_descriptions('https://rs.olx.com.br/regioes-de-porto-alegre-torres-e-santa-cruz-do-sul/autos-e-pecas/carros-vans-e-utilitarios/gol-g4-2008-c-ar-1212506554')
