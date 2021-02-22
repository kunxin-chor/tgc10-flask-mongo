from flask import Flask, render_template, request, redirect, url_for
import os
import pymongo
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

MONGO_URI = os.environ.get('MONGO_URI')
DB_NAME = 'sample_airbnb'

# create the Mongo client
# the purpose of the client is to allow us to connect to the Mongo DB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]


@app.route('/')
def show_listings():

    # retrieve the value of the input named country
    country = request.args.get('country')
    min_beds = request.args.get('min_beds')

    critera = {}

    if country:
        critera['address.country'] = country

    if min_beds:
        critera['beds'] = {
            "$gte": int(min_beds)
        }

    print(critera)

    listings = db.listingsAndReviews.find(critera, {
        'name': 1,
        'summary': 1,
        'images': 1,
        'address': 1,
        'beds': 1
    }).limit(20)
    return render_template('listings.template.html', listings=listings)


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
