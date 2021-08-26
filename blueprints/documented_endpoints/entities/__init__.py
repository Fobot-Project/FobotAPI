from flask import request, jsonify
from flask_restplus import Namespace, Resource, fields, marshal
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
        '''List with all the entities'''
        entity = {}
        entity_list = []
        z = {}
        docs = db.collection('orders').stream()
        for doc in docs:
            Entity = doc.to_dict()
            #entity_list.append("Order_ID")
            entity_list.append(doc.id)
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