"""CRUD OPERATIONS"""

#Importing flask module

from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import urllib.parse

#Creating Flask Object
app = Flask(__name__)

#Connecting to database ,configuring
app.config['MONGO_DBNAME'] = 'donamol'
app.config['MONGO_URI'] = 'mongodb://donaa:'+urllib.parse.quote('anod@20')+'@ds141320.mlab.com:41320/donamol'

#Connecting Pymongo to Mongodb server
mongo = PyMongo(app)

#Defining the route for GET,POST,DELETE.PATCH
@app.route('/user', methods=['GET', 'POST', 'DELETE', 'PATCH'])
def user():
    #Displaying values using method GET
    if request.method == 'GET':
        data = mongo.db.users
        output = []
        for s in data.find():
            output.append({'name' : s['name'], 'email' : s['email']})
        return jsonify(output)
 
    #Inserting values using method POST
    data = request.get_json()
    if request.method == 'POST':
        users = mongo.db.users
        name=request.json['name']
        email=request.json['email']
        s = users.find_one({'name' : name})
        if s:
            return jsonify({'ok': False, 'message': 'User already exist!'})
        else:
            mongo.db.users.insert({'name': name,'email': email})
            return jsonify({'ok': True, 'message': 'User created successfully!'}), 200
          
    #Deleting values using method DELETE
    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response= mongo.db.users.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400
    
    
    #Updating values using method PATCH
    if request.method == 'PATCH':
        users = mongo.db.users
        name=request.json['name']
        distance=request.json['email']
        s = users.find_one({'name' : name})
        if s:
            output = {'name' : s['name'], 'email' : email}
            users.update({"name" : s['name']},{'$set':{"email" : email}})
        else:
            output = "No such name"
            return jsonify( output)

#Start the app running
if __name__ == '__main__':
    app.run(debug=True)
