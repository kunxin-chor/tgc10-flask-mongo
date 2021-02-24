from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
import pymongo

load_dotenv()

app = Flask(__name__)
MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'tgc10_new_shelter'

client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]


@app.route('/animals')
def show_all_animals():
    animals = db.animals.find()
    return render_template('show_animals.template.html', animals=animals)


@app.route('/animals/create')
def show_create_animals():
    return render_template('create_animals.template.html')


@app.route('/animals/create', methods=["POST"])
def process_create_animals():
    name = request.form.get('name')
    breed = request.form.get('breed')
    age = float(request.form.get('age'))
    animal_type = request.form.get('type')

    # insert only ONE new document
    db.animals.insert_one({
        "name": name,
        "age": age,
        "breed": breed,
        "type": animal_type
    })

    return "New animal saved"


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'), port=os.environ.get('PORT'), debug=True)
