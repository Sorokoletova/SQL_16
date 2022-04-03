from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from function import get_open_json
from fixtures import data
from sqlalchemy.orm import relationship
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lesson16.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    email = db.Column(db.String, unique=True)
    role = db.Column(db.String(100))
    phone = db.Column(db.String(20), unique=True)

    def serialize(self):
        return {"id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "age": self.age,
                "email": self.email,
                "role": self.role,
                "phone": self.phone}


# db.drop_all()
# db.create_all()
users_data = get_open_json(data.USERS_DATA)
for user in users_data:
    new_user = User(id=user["id"],
                    first_name=user["first_name"],
                    last_name=user["last_name"],
                    age=user["age"],
                    email=user["email"],
                    role=user["role"],
                    phone=user["phone"])

    # db.session.add(new_user)


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String)
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    customer = relationship('User', foreign_keys='Order.customer_id')
    executor = relationship('User', foreign_keys='Order.executor_id')

    def serialize(self):
        return {"id": self.id,
                "name": self.name,
                "description": self.description,
                "start_date": self.start_date.isoformat(),
                "end_date": self.end_date.isoformat(),
                "address ": self.address,
                "price": self.price,
                "customer_id": self.customer_id,
                "executor_id": self.executor_id}


# db.drop_all()
# db.create_all()

orders_data = get_open_json(data.ORDERS_DATA)
for order in orders_data:
    new_order = Order(id=order["id"],
                      name=order["name"],
                      description=order["description"],
                      start_date=datetime.strptime(order["start_date"], '%m/%d/%Y'),
                      end_date=datetime.strptime(order["end_date"], '%m/%d/%Y'),
                      address=order["address"],
                      price=order["price"],
                      customer_id=order["customer_id"],
                      executor_id=order["executor_id"])

    # db.session.add(new_order)


class Offer(db.Model):
    __tablename__ = "offers"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order = db.relationship("Order")
    executor = db.relationship("User")

    def serialize(self):
        return {"id": self.id,
                "order_id": self.order_id,
                "executor_id": self.executor_id}


# db.drop_all()
# db.create_all()

offers_data = get_open_json(data.OFFERS_DATA)
for offer in offers_data:
    new_offer = Offer(id=offer["id"],
                      order_id=offer["order_id"],
                      executor_id=offer["executor_id"])
    # db.session.add(new_offer)

# db.session.commit()
if __name__ == '__main__':
    app.run(debug=True)
