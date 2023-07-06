#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = []
    for bakery in Bakery.query.all():
        bakery_dict = {
            "id":bakery.id,
            "name":bakery.name,
            "created_at":bakery.created_at
        }
        bakeries.append(bakery_dict)
    response = make_response(
        bakeries, 
        200, 
        {"Content-Type":"application/json"}
    )
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()
    bakery_dict = {
        "id":bakery.id,
        "name":bakery.name,  
        "created_at":bakery.created_at
    }
    response = make_response(
        bakery_dict,
        200,
        {"Content-Type":"application/json"}
    )
    return response


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goodslist = []
    for goods in BakedGood.query.order_by(BakedGood.price.desc()).all():
        goods_dict = {
        "bakery_id": goods.bakery_id,
        "created_at": goods.created_at,
        "id": goods.id,
        "name": goods.name,
        "price": goods.price,
        "updated_at": goods.updated_at
        }
        goodslist.append(goods_dict)
    response = make_response(
        goodslist,
        200,
        {"Content-Type":"application/json"}
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).first()
    goods_dict = {
    "bakery_id": goods.bakery_id,
    "created_at": goods.created_at,
    "id": goods.id,
    "name": goods.name,
    "price": goods.price,
    "updated_at": goods.updated_at
    }    
    response = make_response(
        goods_dict,
        200,
        {"Content-Type":"application/json"}
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
