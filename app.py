from flask import Flask, jsonify, request, render_template
from flaskapp.routes import app_submition


app = Flask(__name__)
from flask_cors import CORS

# Configure CORS to allow requests from all origins
cors = CORS(app)

@app.route('/')
def host():
    return render_template("index.html")

#create user by post method
@app.route('/upload',methods=['POST'])
def postData():
    return app_submition.upload()


@app.route('/send_app_data',methods=['GET'])
def send_app_data():
    return app_submition.send_app_data()

if __name__ == "__main__":
    app.run(port=2700) 