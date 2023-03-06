import firebase_admin
from firebase_admin import db

cred = firebase_admin.credentials.Certificate("model/firebase.json")

default_app = firebase_admin.initialize_app(
    cred,
    {'databaseURL': 'https://cookie-bb3f9-default-rtdb.europe-west1.firebasedatabase.app/'})

predictions = db.reference('/predictions')
