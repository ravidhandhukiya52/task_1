
from flask import Flask, make_response, jsonify, request, redirect, url_for
from flask.views import MethodView
import csv
import json

app = Flask(__name__)

data = {}
file= r'inventory.csv'
with open(file, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for rows in csvReader:
            key = rows['id']
            data[key] = rows


inventory = json.dumps(data, indent=4)

class InventoryApi(MethodView):
    """ /api/inventory """

    def get(self):
        """ Return the entire inventory collection """
        return make_response(inventory, 200)
    

class InventoryItemApi(MethodView):
    """ /api/inventory/<item_name> """

    error = {
        "itemNotFound": {
            "errorCode": "itemNotFound",
            "errorMessage": "Item not found"
        },
        "itemAlreadyExists": {
            "errorCode": "itemAlreadyExists",
            "errorMessage": "Could not create item. Item already exists"
        }
    }

    def get(self, item_name):
        """ Get an item """
        if not data.get(item_name, None):
            return make_response(jsonify(self.error["itemNotFound"]), 400)
        return make_response(jsonify(inventory[item_name]), 200)


app.add_url_rule("/api/inventory", view_func=InventoryApi.as_view("inventory_api"))
app.add_url_rule("/api/inventory/<item_name>", view_func=InventoryItemApi.as_view("inventory_item_api"))

if __name__ == "__main__":
    app.run()