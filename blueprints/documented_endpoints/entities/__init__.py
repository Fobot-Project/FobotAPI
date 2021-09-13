from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields, marshal
from http import HTTPStatus
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
cred = credentials.Certificate({
    "type": "service_account",
    "project_id": "test-bot-hldq",
    "private_key_id": "3d8d3f262081cf5bcf53db00ad1df00d8cee48f5",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCb6J6ITBy1f0ph\nPF/t+OrDOy5p5tP2oV3KSz6HSq2le7ao6usn1W3TpY+KZJ4+WGocxxAACiV7ckc6\ngCgfuJmdlUVQuRjLHVtVo50jVTGNTrkVUGTqeljRbVQR5wpt1jzfyQWs0+BuBFur\nLea/xMT9KVqFAJmHQGNyWSEI+niM6jmOfaUVibhrVW82+XB60HONj3zkGAxloo0C\nP+NZ24Gpf57cyPvV6VEyMjW5lJeWLubSuygp+AnCun0czNCpcjMksqn/m9NJp4Wb\nwK2pv7WHf7if+q1HBdsqcW9XoX22KFtTgEWx3PQrN9a0rxUOI1LoNbjF3TRBmHKh\nMMjJHViLAgMBAAECggEARUgq4sCH5XOKVwlgS7zYfidXacIkoS12I0YqpC5gWfBO\n7GNwWkQyyOGCluo9k9DwXpdrGclofKH82xdGPUpoISnLIqMOTHxgMP9C/geGvJem\nEb2nCreRrocZ29bCwKp6ZKvM9M82pU0Ue04rgz5ql2GAEyiAESVgy9iloHrFhUCC\n0f5+eW2Ky9oKFaNkpcVd5RdZnl1ruPFyXIiFumbNiYO/RP34GFE9WA9vyyQLmgxz\n5fu80G2dsqqY5Na+dMpG8Jk0SXdBJY5CqTO+78gaO6kd9eOs2tX33+jsVrIQMYFJ\nRDYRUoZIqil6+H/lQvg3Jbohh4swCbfcn3A8MwYXIQKBgQDRNB8C2LSA7GhVlr7w\nvI3LijdABPLgYofxolLmLqqf3L+05IneLWmAD9Tri66jT81/Be2rDL+2FHQAco9y\n8tyiA8W7Ny0DrNvDVKqQU0cWnVAxIZtDJVNCilEFhSAcVeKlFN6EncSiBAOQdYnx\n/fFGMK1Ss0D8Wi7ckgU4yNnbOwKBgQC+yJso3t+I3TrglGR/Hh5Wc94Am5vkmvR2\nj6P5cTo3xmRLZRqDI8WEqi0wxS5Id7YQumzk1Fg5zLRsIGkzYhpdSNUM7YOuvQkC\nANkpUrelqLZgN/BwcoaqMIkWC5YJ31T5T2+cEOzXqAZaSeoTt3HFAZIymXt6aYcD\nWvGeuPaC8QKBgQCAdVK9ereLmp6OP5xLUlx3KQ23/9HrOlVjaFsjAHDA7NnCh7qo\ndJYdjpsdb43ytePnJYrEx3VIptJ8G9w9pycXTN2zkbPQV+oxzOFW8evq1PoS0SH3\nXwn7B9esXgxTmeEroN7p6758BZ7yq1njAB2RDf6/k1ZKHk48HmWacqpjVQKBgD7W\nsFRr5FCeHZBvEBLWhsOO8mZc2qIXb8HFWgsFAlnwnIRAztS26Y3ix3Oy3qW72Fn2\nLXvJfS28gQjEPCJSg8CKBrJ1YNQjK15fjSeROS/1O+zBQA6pijVwOxbpxgeGaeSc\nB3TuFjSKAV2nztOjrnNnKxJDf2o4a+HtCHxxC7DhAoGBALJe1CzSZf/IQdeBp1V8\nghxUB4I1lqdn7MfYyPzKWvwQsOfEXdGthcewMCEvP8Vns4Kb3YmlyPJse2fkc4cP\nvNII5yl8Mtp701N1VBuEhIuTqp26PW82FLJ3EvbHNih+dzTmwsIlNd7aOtwT8N/W\nTN9aLCUS+eZnUXI1PKRppF3E\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-mgalh@test-bot-hldq.iam.gserviceaccount.com",
    "client_id": "111431548336381167844",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-mgalh%40test-bot-hldq.iam.gserviceaccount.com"
    })
firebase_admin.initialize_app(cred)
db = firestore.client()
namespace = Namespace('entities', 'Entities fake endpoints')

entity_model = namespace.model('Entity', {

    'food': fields.String(
        required=True,
        description='Entity name'
    ),
    'price': fields.String(
        required=True,
        description='Entity name'
    )
})

entity_list_model = namespace.model('EntityList', {
    'entities': fields.Nested(
        entity_model,
        description='List of entities',
        as_list=True
    ),
    
})

entity_example = {'id': 1, 'name': 'Entity name'}

@namespace.route('')
class entities(Resource):
    '''Get entities list and create new entities'''

    @namespace.response(500, 'Internal Server error')
    #@namespace.marshal_list_with(entity_list_model)
    def get(self):
        '''List with all the orders'''
        entity_list=[]
        user = db.collection('User').document('v0cQnOfc7aJMHTbxSJIh')
        restaurants = user.collection('Restaurants').document('Eg4g9cCZBDuQf1cmS56K')
        orders = restaurants.collection('Order').stream()
        for order in orders:
            Entity = order.to_dict()
            entity_list.append(Entity)

        return {
            'Order information': entity_list
        }

@namespace.route('/<string:menuID>')
class entities(Resource):
    @namespace.response(400, 'Entity with the given name already exists')
    @namespace.response(500, 'Internal Server error')
    @namespace.expect(entity_list_model, validate=True)
    #@namespace.marshal_with(entity_list_model)#, code=HTTPStatus.CREATED)
    def post(self,menuID):
        '''Create a new menu'''
        menu_ref = db.collection(u'menus').document()
        newlist=namespace.payload
        menu_ref.set(
                    newlist            
                )
        
        return newlist
        

@namespace.route('/<string:entity_id>')
class entity(Resource):
    '''Read, update and delete a specific entity'''

    @namespace.response(404, 'Entity not found')
    @namespace.response(500, 'Internal Server error')
    #@namespace.marshal_with(entity_model)
    def get(self):
        '''Get entity_example information'''
        snapshot = db.collection('orders').document(entity_id).get()
        entity_list = snapshot.to_dict()
        return {
            'Order information': entity_list
            
        }

    @namespace.response(400, 'Entity with the given name already exists')
    @namespace.response(404, 'Entity not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.expect(entity_model, validate=True)
    @namespace.marshal_with(entity_model)
    def put(self, entity_id):
        '''Update menu'''
        menu_ref = db.collection(u'menus').document(entity_id)
        newlist=namespace.payload
        menu_ref.update(
                 newlist
                    )
        return newlist

    @namespace.response(204, 'Request Success (No Content)')
    @namespace.response(404, 'Entity not found')
    @namespace.response(500, 'Internal Server error')
    def delete(self, entity_id):
        '''Delete a specific entity'''

        return '', 204