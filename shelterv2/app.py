from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
import pymongo
import datetime

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
                           all_breeds=all_breeds, old_values={})


@app.route('/animals/create', methods=["POST"])
def process_create_animals():
    # name cannot be blank (i.e, empty)
    name = request.form.get('name')
    breed = request.form.get('breed')
    # cannot be less than 0, maybe could be measured in months
    age = request.form.get('age')
    animal_type = request.form.get('type')

    # validation
    # we use a dictionary to store all the errors
    errors = {}

    if len(name) == 0:
        # the key of the key/value pair is the type of the error
        # and the value is what we want to display to the user
        errors['name_is_blank'] = "Animal name cannot be blank"

    if len(age) == 0:
        errors['age_is_blank'] = "Age cannot be blank"

    # we do the next check only if age is not blank
    if len(age) > 0 and float(age) < 0:
        errors['age_is_less_than_0'] = "Animal age cannot be less than zero"

    # insert only ONE new document
    if len(errors) == 0:
        db.animals.insert_one({
            "name": name,
            "age": float(age),
            "breed": breed,
            "type": animal_type
        })
        flash("New animal has been created successfully!")
        return redirect(url_for('show_all_animals'))
    else:
        # redisplay the create animal form template if there is an error
        # we also pass in the errors to the template as well
        all_breeds = db.animal_breeds.find()
        return render_template('create_animals.template.html',
                               all_breeds=all_breeds, errors=errors,
                               old_values=request.form)


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

    # name cannot be blank (i.e, empty)
    name = request.form.get('name')
    breed = request.form.get('breed')
    # cannot be less than 0, maybe could be measured in months
    age = request.form.get('age')
    animal_type = request.form.get('type')

    # validation
    # we use a dictionary to store all the errors
    errors = {}

    if len(name) == 0:
        # the key of the key/value pair is the type of the error
        # and the value is what we want to display to the user
        errors['name_is_blank'] = "Animal name cannot be blank"

    if len(age) == 0:
        errors['age_is_blank'] = "Age cannot be blank"

    # we do the next check only if age is not blank
    if len(age) > 0 and float(age) < 0:
        errors['age_is_less_than_0'] = "Animal age cannot be less than zero"

    if len(errors) == 0:
        db.animals.update_one({
            "_id": ObjectId(animal_id)
        }, {
            '$set': {
                "name": name,
                "age": float(age),
                "breed": breed,
                "type": type
            }
        })
        flash("Animal has been updated successfully.")
        return redirect(url_for('show_all_animals'))
    else:
     
        all_breeds = db.animal_breeds.find()
        animal_to_edit = db.animals.find_one({
            '_id': ObjectId(animal_id)
        })
        old_values = {**animal_to_edit, **request.form}
        return render_template('show_update_animal.template.html',
                               animal_to_edit=old_values,
                               all_breeds=all_breeds,
                               errors=errors)


@app.route('/animals/<animal_id>/checkups')
def show_animal_checkups(animal_id):
    animal = db.animals.find_one({
        "_id": ObjectId(animal_id)
    })
    return render_template('show_animal_checkups.template.html',
                           animal=animal)


@app.route('/animals/<animal_id>/checkups/create')
def show_add_checkup(animal_id):
    animal = db.animals.find_one({
        "_id": ObjectId(animal_id)
    })
    return render_template('add_checkup.template.html', animal=animal)


@app.route('/animals/<animal_id>/checkups/create', methods=['POST'])
def process_add_checkup(animal_id):
    db.animals.update_one({
        "_id": ObjectId(animal_id)
    }, {
        "$push": {
            "checkups": {
                'checkup_id': ObjectId(),
                "vet": request.form.get('vet_name'),
                "diagnosis": request.form.get('diagnosis'),
                "treatment": request.form.get('treatment'),
                "date": datetime.datetime.strptime(request.form.get('date'),
                                                   '%Y-%m-%d')
            }
        }
    })
    flash("New checkup added!")
    return redirect(url_for('show_animal_checkups', animal_id=animal_id))


@app.route('/animal/<animal_id>/checkups/<checkup_id>/delete')
def delete_checkup(animal_id, checkup_id):
    db.animals.update_one({
        "checkups.checkup_id": ObjectId(checkup_id)
    }, {
        '$pull': {
            'checkups': {
                'checkup_id': ObjectId(checkup_id)
            }
        }
    })
    flash("Checkup deleted")
    return redirect(url_for('show_animal_checkups', animal_id=animal_id))


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'), debug=True)
