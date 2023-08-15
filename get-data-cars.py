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

price_max = "16000"
price_min = "10000"

link_face = (
    "https://www.facebook.com/marketplace/109764205717440/carros?minPrice="
    + price_min
    + "&maxPrice="
    + price_max
    + "&exact=false"
)
link_olx = (
    "https://www.olx.com.br/autos-e-pecas/carros-vans-e-utilitarios/estado-rs?pe="
    + price_max
    + "&ps="
    + price_min
)
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


def links(url):
    r = session.get(url)
    for link in r.html.absolute_links:
        if "o=" in link:
            links_olx.append(link)


def facebook(url):
    r = session.get(url)
    r.html.render(scrolldown=30, sleep=2)
    cars = r.html.find(
        ".x9f619.x78zum5.x1r8uery.xdt5ytf.x1iyjqo2.xs83m0k.x1e558r4.x150jy0e.x1iorvi4.xjkvuk6.xnpuxes.x291uyu.x1uepa24"
    )
    for car in cars:
        soup = BeautifulSoup(car.html, "html.parser")

        price = soup.find(
            "span",
            class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u",
        )
        title = soup.find(
            "span",
            class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6",
        )
        region_km = soup.find_all(
            "span",
            class_="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84",
        )

        try:
            data["Price"].append(price.text)
        except AttributeError:
            data["Price"].append(None)

        try:
            data["Title"].append(title.text)
        except AttributeError:
            data["Title"].append(None)

        try:
            data["Region"].append(region_km[0].text)
        except AttributeError:
            data["Region"].append(None)
        except IndexError:
            data["Region"].append(None)

        try:
            data["Km"].append(region_km[1].text)
        except AttributeError:
            data["Km"].append(None)
        except IndexError:
            data["Km"].append(None)

        try:
            link = "https://www.facebook.com/" + list(car.find("a")[0].links)[0]
            data["Link"].append(link)
        except AttributeError:
            data["Link"].append(None)
        except IndexError:
            data["Link"].append(None)

        rest = facebook_description(link)

        data["Date"].append(today.strftime("%d/%m/%Y"))

        data["Year"].append(None)
        data["Description"].append(rest)
        data["CEP"].append(None)
        data["City"].append(None)
        data["Model"].append(None)
        data["Type Car"].append(None)
        data["Power"].append(None)
        data["Color"].append(None)
        data["Doors"].append(None)
        data["Steering"].append(None)
        data["Optional"].append(None)

    return data


def facebook_description(url):
    r = session.get(url)
    r.html.encoding = "utf-8"
    try:
        utf16_html = r.html.html.encode("utf-16", "surrogatepass")
        utf8_html = utf16_html.decode("utf-16").encode("utf-8")
        r.html.html = utf8_html.decode("utf-8")
        r.html.render(sleep=1)
    except Exception as e:
        print("Erro:", e)
    try:
        description = r.html.find(".xz9dl7a.x4uap5.xsag5q8.xkhd6sd.x126k92a")[0].text
    except IndexError:
        description = None

    return description


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
        type_car = dict_description["Tipo de veículo"]
    except KeyError:
        type_car = None
    try:
        power = dict_description["Potência do motor"]
    except KeyError:
        power = None
    try:
        color = dict_description["Cor"]
    except KeyError:
        color = None
    try:
        doors = dict_description["Portas"]
    except KeyError:
        doors = None
    try:
        steering = dict_description["Tipo de direção"]
    except KeyError:
        steering = None
    try:
        complet_model = dict_description["Modelo"]
    except KeyError:
        complet_model = None
    try:
        price = r.html.find(".ad__sc-1leoitd-0.bJHaGt.sc-hSdWYo.dDGSHH")[0].text
    except KeyError:
        price = None
    except IndexError:
        price = None

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
        price,
    )


def olx(url):
    r = session.get(url)
    for html in r.html:
        html.render(sleep=2)
        cars = r.html.find(".horizontal.sc-eLdqWK.bEwpxZ")
        for car in cars:
            title = car.find("h2")[0].text
            region = car.find("p")[0].text
            region = (
                car.find("p")[-2].text
                if "R$" in region or "Profissional" in region or "online" in region
                else region
            )
            km = car.find("li")[0].text
            year = car.find("li")[1].text
            link = list(car.find("a")[0].links)[0]
            # return a 'set', so i need transform in list

            rest = olx_descriptions(link)

            data["Km"].append(km)
            data["Year"].append(year)
            data["Price"].append(rest[10])
            data["Region"].append(region)
            data["Title"].append(title)
            data["Link"].append(link)
            data["Description"].append(rest[0])
            data["CEP"].append(rest[1])
            data["City"].append(rest[2])
            data["Model"].append(rest[3])
            data["Type Car"].append(rest[4])
            data["Power"].append(rest[5])
            data["Color"].append(rest[6])
            data["Doors"].append(rest[7])
            data["Steering"].append(rest[8])
            data["Optional"].append(rest[9])
            data["Date"].append(today.strftime("%d/%m/%Y"))

    return data


links(link_olx)
for link in links_olx:
    olx(link)
facebook(link_face)

df = pd.DataFrame.from_dict(data).to_excel(ABSOLUT_PATH, index=False)
