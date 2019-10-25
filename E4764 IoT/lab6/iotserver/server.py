from flask import Flask, render_template
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import json

app= Flask(__name__)

app.config['MONGO_DBNAME']= 'coordinates'
app.config['MONGO_URI']= 'mongodb://localhost:27017/coordinates'
mongo= PyMongo(app)

@app.route('/post', methods=['POST'])
def add_coordinate():   
    '''
    columbia c=1 o=2 l=3 u=4 m=5 b=6 i =7 a=8
    '''
    xcoordinate=0
    ycoordinate=0
    coordinate= mongo.db.coordinates
    
    label = request.json["label"]
    xcoordinate= request.json["x"]
    ycoordinate= request.json["y"]
    
    print(label)
    print(xcoordinate) 
    print(ycoordinate) 
    
    coordinate.insert({'label':label,'xcoordinate': xcoordinate, 'ycoordinate': ycoordinate})
    '''
    new_coordinate=coordinate.find_one({'label': label} and {'xcoordinate': xcoordinate} and {'ycoordinate':ycoordinate})
    output = {'label':new_coordinate['label'], 'xcoordinate': new_coordinate['xcoordinate'],'ycoordinate':new_coordinate['ycoordinate']}
    '''
    return jsonify({})


@app.route('/get', methods=['GET'])
def get_coordinate():
    coordinate= mongo.db.coordinates
    output= []
    for c in coordinate.find():
        output.append({'label':c['label'],'xcoordinate': c['xcoordinate'], 'ycoordinate': c['ycoordinate']}) 
    return jsonify({'result' : output})


if __name__== '__main__':
    app.run(debug=True, host="0.0.0.0", port= 8080)


