from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields
from http import HTTPStatus
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
cred = credentials.Certificate({
    
  })
firebase_admin.initialize_app(cred)
db = firestore.client()
namespace = Namespace('entities', 'Entities fake endpoints')

entity_model = namespace.model('Entity', {
    'id': fields.String(
        readonly=True,
        description='Entity identifier'
    ),
    'food': fields.String(
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
    'total_records': fields.Integer(
        description='Total number of entities',
    ),
})

entity_example = {'id': 1, 'name': 'Entity name'}

@namespace.route('')
class entities(Resource):
    '''Get entities list and create new entities'''

    @namespace.response(500, 'Internal Server error')
    @namespace.marshal_list_with(entity_list_model)
    def get(self):
        '''List with all the entities'''
        snapshot = db.collection('orders').document('9313a565-3839-2595-8175-c072eadd92d7').get()
        entity_list = snapshot.to_dict()
        return {
            'entities': entity_list,
            
        }

    @namespace.response(400, 'Entity with the given name already exists')
    @namespace.response(500, 'Internal Server error')
    @namespace.expect(entity_model)
    @namespace.marshal_with(entity_model, code=HTTPStatus.CREATED)
    def post(self):
        '''Create a new entity'''

        if request.json['name'] == 'Entity name':
            namespace.abort(400, 'Entity with the given name already exists')

        return entity_example, 201

@namespace.route('/<int:entity_id>')
class entity(Resource):
    '''Read, update and delete a specific entity'''

    @namespace.response(404, 'Entity not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.marshal_with(entity_model)
    def get(self, entity_id):
        '''Get entity_example information'''

        return entity_example

    @namespace.response(400, 'Entity with the given name already exists')
    @namespace.response(404, 'Entity not found')
    @namespace.response(500, 'Internal Server error')
    @namespace.expect(entity_model, validate=True)
    @namespace.marshal_with(entity_model)
    def put(self, entity_id):
        '''Update entity information'''

        if request.json['name'] == 'Entity name':
            namespace.abort(400, 'Entity with the given name already exists')

        return entity_example

    @namespace.response(204, 'Request Success (No Content)')
    @namespace.response(404, 'Entity not found')
    @namespace.response(500, 'Internal Server error')
    def delete(self, entity_id):
        '''Delete a specific entity'''

        return '', 204