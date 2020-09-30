import pandas as pd
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import pickle


def numbers_to_class(argument):
    switcher = {
        0: "Evertek M10 Lite",
        1: "Huawei Nova 7i",
        2: "No values",
        3: "Huawei Y6 Prime 2019",
        4: "Huawei Y6s 2019",
        5: "Huawei Y6s (2019)",
        6: "Huawei Y7 Prime 2019",
        7: "Huawei Y7p",
        8: "Huawei Y8p",
        9: "Huawei Y9 Prime 2019",
        10: "No values",
        11: "Huawei Y9s",
        12: "Iku A30",
        13: "Infinix Hot 8 ",
        14: "Infinix Hot 9",
        15: "Infinix Hot 9 Play",
        16: "Infinix Note 7",
        17: "Logicom Le Posh 178",
        18: "Logicom Le Posh 178",
        19: "Logicom Téléphone Portable POSH 280",
        20: "Nokia 105 ( 2019 )",
        21: "Nokia 4.2 ",
        22: "Nokia 5310 ",
        23: "Nokia C1",
        24: "Nokia C2",
        25: "Oppo A3",
        26: "Oppo A31",
        27: "Oppo A9 (2020)",
        28: "Samsung A11",
        29: "Samsung Galaxy A01",
        30: "Samsung Galaxy A20s",
        31: "Samsung Galaxy A51",
        32: "Samsung Galaxy S10 plus",
        33: "Samsung M11",
        34: "Tecno Camon 15",
        35: "Tecno Camon 15 Pro",
        36: "Tecno Pop 3 Plus",
        37: "Tecno Spark 4 Lite",
        38: "Tecno Spark 5 Air",
        39: "Tecno Spark 5 pro ",
        40: "ZTE Blade V10 Vita "
    }
    return switcher.get(argument)


class Similarity(Resource):

    def post(self):
        postedData = request.get_json()

        marque = postedData['marque']
        marque = marque['value']
        prix = postedData['prix']

        ecran = postedData['ecran']
        ecran = ecran['value']
        ram = postedData['ram']
        ram = ram['value']
        rom = postedData['rom']
        rom = rom['value']
        couleur = postedData['couleur']
        couleur = couleur['value']

        df_test = pd.DataFrame({'marque': ["{}".format(marque)], 'name': ["Samsung M11"], 'price': [
            "{}".format(prix)], 'ecran': ["{}".format(ecran)], 'Ram': ["{}".format(ram)],
            'Rom': ["{}".format(rom)], 'couleur': ["{}".format(couleur)]})

        df_to_encod = pd.DataFrame(
            [[df_test.iloc[0][0], df_test.iloc[0][6]]], columns=['marque', 'couleur'])

        df_deploy = df_to_encod
        file = open("dict_all.obj", 'rb')
        enc_loaded = pickle.load(file)
        file.close()

        for col in df_deploy.columns:
            df_deploy.replace(enc_loaded[col], inplace=True)
        df_train = pd.DataFrame(df_deploy['marque'], columns=['marque'])

        df_train["price"] = df_test["price"]
        df_train["ecran"] = df_test["ecran"]
        df_train["Ram"] = df_test["Ram"]
        df_train["Rom"] = df_test["Rom"]
        df_train["couleur"] = df_deploy['couleur']
        # Load the Model back from file
        Pkl_Filename = "knnModel.pkl"
        with open(Pkl_Filename, 'rb') as file:
            Pickled_knn_Model = pickle.load(file)
        predict = Pickled_knn_Model.predict(df_train)

        pred = numbers_to_class(predict[0])

        retJson = {
            "status": 200,
            "message": "Succesfuly signed up for this api",

            "predict": pred,



        }

        return jsonify(retJson)
