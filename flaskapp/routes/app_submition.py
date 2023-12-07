from flask import Flask, request, jsonify, render_template
from flaskapp.utils.post_to_firebase_storage import upload_file, delete_app
from con_mongodb import con

myClient = con()
myCol = myClient['apps']
head = False

def upload():
    app_images_urls = []
    app_icon_url = None
    app_images = []
    app_apk_url = None
    
    # Get key-value pairs from FormData
    app_name = request.form.get('app_name')
    if myCol.find_one({"app_name": app_name}):
            return jsonify("app already exist!"),404
    else:
        app_description = request.form.get('app_description')

        # Handle app_icon file
        if 'app_icon' in request.files:
            app_icon = request.files['app_icon']
            app_icon_extension = app_icon.filename.rsplit('.', 1)[1].lower()
            app_icon_url = upload_file(app_icon, app_name+"/icon/"+app_name+"."+app_icon_extension)
        else:
            return jsonify("app_icon not found!"),404

        # Handle app_images files
        if 'app_images' in request.files:
            app_images = request.files.getlist('app_images')
            i = 0
            for x in app_images:
                app_images_extension = x.filename.rsplit('.', 1)[1].lower()
                app_image_url = upload_file(x, app_name+"/images/"+app_name+str(i)+"."+app_images_extension)
                app_images_urls.append(app_image_url)
                i += 1
        else:
            delete_app(app_name)
            return jsonify("app_images not found!"),404

        # Handle app_apk file
        if 'app_apk' in request.files:
            app_apk = request.files['app_apk']
            app_apk_extension = app_apk.filename.rsplit('.', 1)[1].lower()
            if app_apk_extension == "apk":
                app_apk_url = upload_file(app_apk, app_name+"/apk/"+app_name+".apk")
            else:
                return jsonify("upload apk file, submitted file was not an apk file"),404
        else:
            delete_app(app_name)
            return jsonify("app_apk not found!"),404


        try:
            countD = myCol.count_documents({})
            myCol.insert_one({"_id": countD, "app_name": app_name, "app_description": app_description, "app_icon_url": app_icon_url, "app_images_urls": app_images_urls, "app_apk_url": app_apk_url})
            resp = jsonify("data inserted!")
            resp.status_code = 200
            return resp
        except:
            delete_app(app_name)
            return jsonify("data not inserted successfully!"),404


def send_app_data():
    apps = []
    for id in range(0,myCol.count_documents({})):
        data = myCol.find_one({"_id": id})
        apps.append(data)
    resp = jsonify(apps)
    resp.status_code = 200
    return resp