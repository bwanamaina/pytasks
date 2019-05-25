from flask import Flask, jsonify, request
from pymongo import MongoClient
import dns  # required for connecting with SRV
from bson.objectid import ObjectId

app = Flask(__name__)

username = 'admin'
password = 'aKR0dzjNIeA2mahG'

client = MongoClient(
    'mongodb+srv://' + username + ':'+password+'@cluster0-h74u6.mongodb.net')

database = client.get_database('pymongotasks')
collection = database.tasks


@app.route('/tasks', methods=['GET'])
def get_tasks():

    tasks = collection.find()

    output = []
    for task in tasks:
        output.append({
            'id': str(task['_id']),
            'title': task['title'],
            'description': task['description'],
            'complete': task['complete']
        })

    return jsonify({'result': output})


@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    task = collection.find_one({'_id': ObjectId(id)})

    if task:
        output = {
            'id': str(task['_id']),
            'title': task['title'],
            'description': task['description'],
            'complete': task['complete']
        }
    else:
        output = 'no results found'

    return jsonify({'result': output})


@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = collection.delete_one({'_id': ObjectId(id)})

    if task.deleted_count > 0:
        output = {
            'sucessful': True,
            'message': 'successfully deleted'
        }
    else:
        output = {
            'sucessful': False,
            'message': 'not successfully deleted'
        }

    return jsonify({'result': output})


@app.route('/tasks/<id>', methods=['PATCH'])
def update_task(id):

    title = request.json['title']
    description = request.json['description']
    complete = request.json['complete']

    task = {
        'title': title,
        'description': description,
        'complete': complete
    }

    result = collection.update_one(
        {'_id': ObjectId(id)}, {'$set': task})

    if result.modified_count > 0:
        output = {
            'sucessful': True,
            'message': 'successfully updated'
        }
    else:
        output = {
            'sucessful': False,
            'message': 'not successfully updated'
        }

    return jsonify({'result': output})


@app.route('/tasks', methods=['POST'])
def add_task():

    title = request.json['title']
    description = request.json['description']

    task = {
        'title': title,
        'description': description,
        'complete': False
    }

    inserted_task = collection.insert_one(task)
    task_id = inserted_task.inserted_id

    new_task = collection.find_one({'_id': task_id})

    output = {
        'title': new_task['title'],
        'description': new_task['description'],
        'complete': new_task['complete']
    }
    return jsonify({'result': output})


if __name__ == '__main__':
    app.run(debug=True)
