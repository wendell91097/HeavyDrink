from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Beverage, beverage_schema, beverages_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'giddy': 'up'}

@api.route('/drinks', methods=['POST'])
@token_required
def create_beverage(current_user_token):
    name = request.json['name']
    type = request.json['type']
    price = request.json['price']
    proof = request.json['proof']
    origin = request.json['origin']
    vintage = request.json.get('vintage', 'Blank')
    description = request.json.get('description', 'Blank')
    user_token = current_user_token.token

    beverage = Beverage(name=name, type=type, price=price, proof=proof, origin=origin, vintage=vintage, description=description, user_token=user_token)

    db.session.add(beverage)
    db.session.commit()

    response = beverage_schema.dump(beverage)
    return jsonify(response)

@api.route('/drinks', methods = ['GET'])
@token_required
def get_car(current_user_token):
    a_user = current_user_token.token
    beverages = Beverage.query.filter_by(user_token = a_user).all()
    response = beverage_schema.dump(beverages)
    return jsonify(response)

@api.route('/drinks/<id>', methods = ['GET'])
@token_required
def get_single_contact(current_user_token, id):
    contact = Beverage.query.get(id)
    response = beverage_schema.dump(contact)
    return jsonify(response)

@api.route('/drinks/<id>', methods = ['POST','PUT'])
@token_required
def update_contact(current_user_token,id):
    beverage = Beverage.query.get(id)
    beverage.name = request.json['name']
    beverage.type = request.json['type']
    beverage.price = request.json['price']
    beverage.proof = request.json['proof']
    beverage.origin = request.json['origin']
    beverage.vintage = request.json['vintage']
    beverage.description = request.json['description']
    beverage.user_token = current_user_token.token

    db.session.commit()
    response = beverage_schema.dump(beverage)
    return jsonify(response)

@api.route('/drinks/<id>', methods = ['DELETE'])
@token_required
def delete_contact(current_user_token, id):
    beverage = Beverage.query.get(id)
    db.session.delete(beverage)
    db.session.commit()
    response = beverage_schema.dump(beverage)
    return jsonify(response)
