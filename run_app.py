from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from create_add_table import User, Order, Offer
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lesson16.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.route('/users/', methods=['GET'])
def page_users():
    """выводим все users"""
    users = db.session.query(User).all()
    return jsonify([user.serialize() for user in users])


@app.route('/users/<int:user_id>', methods=['GET'])
def page_user(user_id):
    """выводим users по id"""
    users = db.session.query(User).filter(User.id == user_id).first()
    if users is None:
        return "По запросу данные не найдены."
    return jsonify(users.serialize())


@app.route('/orders/', methods=['GET'])
def page_orders():
    """выводим все orders"""
    orders = db.session.query(Order).all()
    return jsonify([order.serialize() for order in orders])


@app.route('/orders/<int:order_id>', methods=['GET'])
def page_order(order_id):
    """выводим orders по id"""
    orders = db.session.query(Order).filter(Order.id == order_id).first()
    if orders is None:
        return "По запросу данные не найдены."
    return jsonify(orders.serialize())


@app.route('/offers/', methods=['GET'])
def page_offers():
    """выводим все offers"""
    offers = db.session.query(Offer).all()
    return jsonify([offer.serialize() for offer in offers])


@app.route('/offers/<int:offer_id>', methods=['GET'])
def page_offer(offer_id):
    """выводим offers по id"""
    offers = db.session.query(Offer).filter(Offer.id == offer_id).first()
    if offers is None:
        return "По запросу данные не найдены."
    return jsonify(offers.serialize())


@app.route('/users', methods=['POST'])
def add_user():
    """добавляем запись в таблицу users"""
    user = request.json
    db.session.add(User(**user))
    db.session.commit()
    return "Данные добавлены."


@app.route('/offers', methods=['POST'])
def add_offers():
    """добавляем запись в таблицу offers"""
    offer = request.json
    db.session.add(Offer(**offer))
    db.session.commit()
    return "Данные добавлены."


@app.route('/orders', methods=['POST'])
def add_orders():
    """добавляем запись в таблицу orders"""
    order = request.json
    db.session.add(Order(name=order["name"],
                         description=order["description"],
                         start_date=datetime.strptime(order["start_date"], '%m/%d/%Y'),
                         end_date=datetime.strptime(order["end_date"], '%m/%d/%Y'),
                         address=order["address"],
                         price=order["price"],
                         customer_id=order["customer_id"],
                         executor_id=order["executor_id"]))
    db.session.commit()
    return "Данные добавлены."


@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Изменяем запись в таблице users"""
    user = request.json
    find_user = db.session.query(User).filter(User.id == user_id).first()
    if find_user is None:
        return "По запросу данные не найдены."
    db.session.query(User).filter(User.id == user_id).update(user)
    db.session.commit()
    return "Данные Изменены."


@app.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Изменяем запись в таблице orders"""
    order = request.json
    find_order = db.session.query(Order).filter(Order.id == order_id).first()
    if find_order is None:
        return "По запросу данные не найдены."
    if 'start_date' in order:
        order['start_date'] = datetime.strptime(order['start_date'], '%m/%d/%Y').date()
    if 'end_date' in order:
        order['end_date'] = datetime.strptime(order['end_date'], '%m/%d/%Y').date()
    db.session.query(Order).filter(Order.id == order_id).update(order)
    db.session.commit()
    return "Данные Изменены."


@app.route('/offers/<int:offer_id>', methods=['PUT'])
def update_offer(offer_id):
    """Изменяем запись в таблице offers"""
    offer = request.json
    find_offer = db.session.query(Offer).filter(Offer.id == offer_id).first()
    if find_offer is None:
        return "По запросу данные не найдены."
    db.session.query(Offer).filter(Offer.id == offer_id).update(offer)
    db.session.commit()
    return "Данные Изменены."


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Удаляем запись в таблице users"""
    user = db.session.query(User).filter(User.id == user_id).delete()
    db.session.commit()
    return f"удалено записей:{user}"


@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """Удаляем запись в таблице orders"""
    order = db.session.query(Order).filter(Order.id == order_id).delete()
    db.session.commit()
    return f"удалено записей:{order}"


@app.route('/offers/<int:offer_id>', methods=['DELETE'])
def delete_offer(offer_id):
    """Удаляем запись в таблице offers"""
    offer = db.session.query(Offer).filter(Offer.id == offer_id).delete()
    db.session.commit()
    return f"удалено записей:{offer}"


app.run()
