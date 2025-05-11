# Import the required libraries
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('C:\Users\USER\OneDrive\Desktop\security_platform\securityplatform-f08b3-firebase-adminsdk-fbsvc-f95f03ed41.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.Client()

# Your other code goes here