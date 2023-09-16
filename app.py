from flask import Flask, jsonify, request, send_file
from con_mongodb import con


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
    name = _json['name']
    app_description = _json['description']
    category = _json['category']
    image = _json['img_url']
    apk = _json['apk_url']
    countD = myCol.count_documents({})
    if id and name and app_description  and  category and image and apk and request.method == 'POST':
        myCol.insert_one({'_id': countD, 'name': name, 'description': app_description, 'category':category, 'img_url': image, "apk_url": apk}) 
        resp = jsonify('app added successfully')
        resp.status_code = 200
        return resp
    else:
        return not_found()
    

@app.route('/',methods=['GET'])
def getAllData():
    try:
        users =  list(myCol.find())
        resp = jsonify(users)
        resp.status_code = 200
        # resp = dump(users)
        return resp
    except:
        not_found()
        

@app.route('/apk')
def download_apk():
    # Specify the path to your APK file
    apk = request.args.get('apk')
    apk_path = 'assets/'+apk+'/file/'+apk+'.apk'
    
    # Define the desired filename for the downloaded APK
    apk_filename = apk+'.apk'
    
    # Use Flask's send_file function to send the file for download
    return send_file(apk_path, as_attachment=True, download_name=apk_filename)

@app.route('/image')
def apk_image():
    apk = request.args.get('image')
    # Specify the path to your APK image file
    image_path = 'assets/'+apk+'/images/'+apk+'.png'
    
    # Use Flask's send_file function to send the image for display
    return send_file(image_path, mimetype='image/png')

if __name__ == "__main__":
    app.run() 