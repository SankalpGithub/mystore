from flask import Flask, jsonify, request
from con_mongodb import con
from bson.json_util import dumps
from bson.objectid import ObjectId

app = Flask(__name__)
myClient = con()
myCol = myClient['appStore']

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
    if name and app_description and request.method == 'POST':
        myCol.insert_one({'appName': name, 'app_description': app_description}) 
        resp = jsonify('user added successfully')
        resp.status_code = 200        
        return resp
    else:
        return not_found()
    

if __name__ == "__main__":
    app.run() 