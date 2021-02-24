from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
import pymongo

# we can use ObjectId
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
# assign a secret key to setup sessions
app.secret_key = os.environ.get('SECRET_KEY')

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
    all_breeds = db.animal_breeds.find()
    return render_template('create_animals.template.html',
                           all_breeds=all_breeds)


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
    flash("New animal has been created successfully!")
    return redirect(url_for('show_all_animals'))


@app.route('/animals/<animal_id>/delete')
def delete_animal(animal_id):
    # find the animal that we want to delete
    animal = db.animals.find_one({
        '_id': ObjectId(animal_id)
    })

    return render_template('confirm_delete_animal.template.html',
                           animal_to_delete=animal)


@app.route('/animals/<animal_id>/delete', methods=['POST'])
def process_delete_animal(animal_id):
    db.animals.remove({
        "_id": ObjectId(animal_id)
    })
    flash("Animal has been deleted")
    return redirect(url_for('show_all_animals'))


@app.route('/animals/<animal_id>/update')
def show_update_animal(animal_id):
    all_breeds = db.animal_breeds.find()
    animal_to_edit = db.animals.find_one({
        '_id': ObjectId(animal_id)
    })
    return render_template('show_update_animal.template.html',
                           animal_to_edit=animal_to_edit,
                           all_breeds=all_breeds)


@app.route('/animals/<animal_id>/update', methods=["POST"])
def process_update_animal(animal_id):
    db.animals.update_one({
        "_id": ObjectId(animal_id)
    }, {
        '$set': request.form
    })
    flash("Animal has been updated successfully.")
    return redirect(url_for('show_all_animals'))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'), debug=True)
