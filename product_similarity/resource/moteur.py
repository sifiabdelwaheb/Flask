from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import pickle
import re
import time
import pandas as pd


def clean_url(coulum):
    clean = []
    for x in range(len(coulum)):
        for item in coulum[x]:
            clean.append((item))

    return clean


def clean_list(coulum):
    clean = []

    for x in range(len(coulum)):
        for item in coulum[x]:
            clean.append((item.text))

    return clean


def clean_list1(coulum):
    clean = []

    for x in range(len(coulum)):
        for item in coulum[x]:
            clean.append((item.a.text))

    return clean


def clean_discount(coulum):
    clean = []

    for x in range(len(coulum)):
        for item in coulum[x]:
            clean.append((item.text))

    return clean


def clean_prix(coulum):
    clean = []

    for x in range(len(coulum)):
        for item in coulum[x]:
            clean.append((item.text))

    return clean


def clean_car(coulum):
    clean = []

    for x in range(len(coulum)):
        for item in coulum[x]:
            clean.append((item.text))

    return clean


def clean_des(coulum):
    clean = []

    for x in range(len(coulum)):
        for item in coulum[x]:
            clean.append((item.text))

    return clean


def clean_numcom(coulum):
    clean = []

    for x in range(len(coulum)):
        for item in coulum[x]:
            clean.append((item.text))

    return clean


def url_to_transcript1(clean_link):
    response = requests.get(clean_link)
    soup = BeautifulSoup(response.text, "html.parser")

    name = soup.find_all('div', attrs={'class': '-fs0 -pls -prl'})
    details = soup.find_all('div', attrs={'class': 'markup -pam'})
    marque = soup.find_all('div', attrs={'class': '-fs14 -pvxs'})
    price = soup.find_all('span', attrs={'class': '-b -ltr -tal -fs24'})
    discount = soup.find_all('span', attrs={'class': 'tag _dsct _dyn -mls'})
    car = soup.find_all('div', attrs={'class': 'markup -pam'})
    descrptivetechnique = soup.find_all('div', attrs={'class': 'card-b -fh'})
    avis = soup.find_all('div', attrs={'class': 'stars _m -mvs'})
    numcomments = soup.find_all('div', attrs={'class': 'cola -phm -df -d-co'})
    comments = soup.find_all('p', attrs={'class': '-pvs'})

    Name = []
    Deatils = []
    Marque = []
    Prix = []
    Discount = []
    Car = []
    Des = []
    Avis = []
    Numcmts = []
    Cmts = []
    for x in range(len(marque)):
        Name.append(name[x])
        Deatils.append(details[x])
        Marque.append(marque[x])
        Prix.append(price[x])
        Discount.append(discount[x])
        Car.append(car[x])
        Des.append(descrptivetechnique[x])
        # Avis.append(avis[x])
        Numcmts.append(numcomments[x])
        # Cmts.append(comments[x])

    return Name, Deatils, Marque, Prix, Discount, Car, Des, Avis, Numcmts, Cmts


class Moteur(Resource):
    def post(self):
        postedData = request.get_json()

        product = postedData['product']
        value = str(product)+" jumia"
        value = value.replace(' ', '+')
        #executable_path = r'C:\Users\mmcd\chromedriver.exe'
    #    browser = webdriver.Chrome(executable_path=executable_path)

        browser = webdriver.Chrome(ChromeDriverManager().install())

        for i in range(1, 20):
            browser.get("https://www.google.com/search?q=" +
                        value + "&start=" + str(i))
            matched_elements = browser.find_elements_by_xpath(
                '//a[starts-with(@href, "https://www.jumia.")]')
            if matched_elements:
                matched_elements[0].click()
                print(matched_elements[0])
                break

        time.sleep(5)
        links = []
        while True:
            spans_to_iterate = browser.find_elements_by_xpath(
                "//a[contains(@class,'core')]")
            print(spans_to_iterate)
            link_list = []

    # iterate span elements to save the href attribute of a element
            for span in spans_to_iterate:
                link_text = span.get_attribute("href")
                link_list.append(link_text)
                links.append(link_list)

            try:
                if browser.find_element_by_xpath('.//a[@title="Suivant"]'):
                    browser.find_element_by_xpath(
                        './/a[@title="Suivant"]').click()
                    time.sleep(5)

            except:
                break

        clean_link = clean_url(links)
        jumia = [url_to_transcript1(u) for u in clean_link[:3]]

        Name = []
        Deatils = []
        Marque = []
        Prix = []
        Discount = []
        Car = []
        Des = []
        Avis = []
        Numcmts = []
        Cmts = []
        for item in jumia:
            Name.append(item[0])
            Deatils = [].append(item[1])
            Marque.append(item[2])
            Prix.append(item[3])
            Discount.append(item[4])
            Car.append(item[5])
            Des.append(item[6])
            Avis.append(item[7])
            Numcmts.append(item[8])
            Cmts.append(item[9])

        clean_marque = clean_list1(Marque)
        clean_name = clean_list(Name)
        clean_disc = clean_discount(Discount)
        clean_carac = clean_car(Car)
        clean_price = clean_prix(Prix)
        clean_description = clean_des(Des)
        clean_numcommentaire = clean_numcom(Numcmts)
        df = pd.DataFrame(clean_marque, columns=['marque'])
        df["name"] = clean_name
        df["marque"] = clean_marque
        df["Prix"] = clean_price
        df["discount"] = clean_disc
        df["Avis"] = clean_numcommentaire
        df["caracterstique"] = clean_carac
        df["deescriptive"] = clean_description
        df.to_csv(f"{product}.csv", index=False, header=True)

        retJson = {
            "status": 200,
            "message": "Succesfuly signed up for this api",
            "response": {
                "message": "terminer",
                "product": product,



            }
        }

        return jsonify(retJson, 200)
