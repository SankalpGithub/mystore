from firebase_admin import credentials, initialize_app, storage
from dotenv import load_dotenv, dotenv_values
import os
load_dotenv()

# Initialize Firebase Admin SDK
cred = credentials.Certificate(os.getenv("/etc/secrets/firebase_key"))
initialize_app(cred, {'storageBucket': os.getenv("firebase_app_id")})

bucket = storage.bucket()

def upload_file(file, remote_path):
    try:
        # Upload the file
        blob = bucket.blob(remote_path)
        blob.upload_from_file(file)
        download_url = blob.public_url
        return download_url
    except:
        return "faild to upload"

def delete_app(folder_path):
    try:
        blobs = bucket.list_blobs(prefix=folder_path)

        # Delete each file in the folder
        for blob in blobs:
            blob.delete()
    except:
        return "faild to delete"