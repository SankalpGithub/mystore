from firebase_admin import credentials, initialize_app, storage
from dotenv import load_dotenv, dotenv_values
import os
load_dotenv()

# Initialize Firebase Admin SDK
cred = credentials.Certificate(os.getenv("firebase_key_path"))
initialize_app(cred, {'storageBucket': os.getenv("firebase_app_id")})

bucket = storage.bucket()

def upload_file(file, remote_path, content_type):
    try:
        # Upload the file
        blob = bucket.blob(remote_path)
        blob.upload_from_file(file, content_type=content_type)
        blob.make_public()

        # Get the public URL
        download_url = blob.public_url
        return download_url
    except Exception as e:
        return f'Failed to upload: {str(e)}'

def delete_app(folder_path):
    try:
        blobs = bucket.list_blobs(prefix=folder_path)

        # Delete each file in the folder
        for blob in blobs:
            blob.delete()
    except:
        return "faild to delete"