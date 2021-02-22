# Python Mongo Example

## Dependencies
```
pip3 install flask
pip3 install pymongo
pip3 install dnspython
pip3 install python-dotenv
```

## Setup

1. Create a new file named `.env`

2. Put inside `.env` the following:

```
MONGO_URI=<connection string copied from Mongo Atlas>
```

3. Create a mongo client:

```
DB_NAME = 'sample_airbnb'
client = pymongo.MongoClient(MONGO_URI)
```