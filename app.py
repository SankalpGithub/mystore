from flask import Flask, jsonify, request, send_file
from con_mongodb import con
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
myClient = con()
myCol = myClient['apps']

#error function
@app.errorhandler(404)
def not_found(error = None):
    message = {
                'status': 404,'message': 'Not Found ' + request.url
                }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
#create user by post method
@app.route('/postData',methods=['POST'])
def postData():
    _json = request.json
    name = _json['appName']
    app_description = _json['description']
    app_icon = _json['app_icon']
    if name and app_description and request.method == 'POST':
        myCol.insert_one({'appName': name, 'app_description': app_description, 'app_icon': app_icon}) 
        resp = jsonify('user added successfully')
        resp.status_code = 200        
        return resp
    else:
        return not_found()
    
@app.route('/',methods=['GET'])
def getAllData():
    users =  myCol.find()
    resp = dumps(users)
    return resp

@app.route('/download_apk')
def download_apk():
    # Specify the path to your APK file
    apk = request.args.get('apk')
    apk_path = 'assets/apks/'+apk+'.apk'
    
    # Define the desired filename for the downloaded APK
    apk_filename = apk+'.apk'
    
    # Use Flask's send_file function to send the file for download
    return send_file(apk_path, as_attachment=True, download_name=apk_filename)

@app.route('/image')
def apk_image():
    image = request.args.get('image')
    # Specify the path to your APK image file
    image_path = 'assets/images/'+image+'.png'
    
    # Use Flask's send_file function to send the image for display
    return send_file(image_path, mimetype='image/png')

if __name__ == "__main__":
    app.run(port=8080) 