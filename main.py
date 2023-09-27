from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, Flask
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///mydatabase.db'  
db = SQLAlchemy(app)

class Pizza(db.Model):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    restaurant_pizza = db.relationship('RestaurantPizza', backref='pizza')

class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    restaurant_pizza = db.relationship("RestaurantPizza", backref="restaurant")

class RestaurantPizza(db.Model):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/restaurant', methods=["GET"])
def getting_data():
    if request.method == "GET":
        restaurants = Restaurant.query.all()
        restaurant_list = [{"id": restaurant.id, "name": restaurant.name, "address": restaurant.address} for restaurant in restaurants]
        return jsonify(restaurant_list)
    
@app.route('/restaurant/<int:id>', methods=["GET", "DELETE"])
def getting_by_id(id):
    if request.method == "GET":
        restaurant = Restaurant.query.get(id)

        if not restaurant:
            return jsonify({"error": f"Restaurant with ID {id} not found"}), 404

        restaurant_pizzas = RestaurantPizza.query.filter_by(restaurant_id=id).all()
        pizza_list = []

        for res_pizza in restaurant_pizzas:
            pizza = Pizza.query.get(res_pizza.pizza_id)
            if pizza:
                pizza_data = {
                    "id": pizza.id,
                    "name": pizza.name,
                    "ingredients": pizza.ingredients,
                }
                pizza_list.append(pizza_data)

        restaurant_data = {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "pizzas": pizza_list,
        }

        return jsonify(restaurant_data)

    if request.method == "DELETE":
        try:
            restaurant=Restaurant.query.get(id)
            if restaurant:
                db.session.delete(restaurant)
                db.session.commit()
                return jsonify({"message": "Restaurant deleted successfully"}), 200
            else:
                return jsonify({"error": f"Restaurant with ID {id} not found"}), 404
        except Exception as e:
            return jsonify({"error": "Error occurred"}), 500
        

@app.route('/pizza', methods=["GET"])     
def get_pizza():
    if request.method == "GET":
        pizzas=Pizza.query.all()
        pizza_list=[{"id":pizza.id, "name":pizza.name, "ingredients":pizza.ingredients, "created":pizza.date_created, "updated":pizza.updated} for pizza in pizzas]
        return jsonify(pizza_list)

@app.route('/pizza_restaurants', methods=["POST"])
def post_pizzaRest():
    if request.method == "POST":
        try:
            data = request.get_json()

          
            pizza_id = data.get('pizza_id')
            restaurant_id = data.get('restaurant_id')
            price = data.get('price')

            
            pizza = Pizza.query.get(pizza_id)
            restaurant = Restaurant.query.get(restaurant_id)

            if not pizza:
                return jsonify({"error": f"Pizza with ID {pizza_id} not found"}), 404

            if not restaurant:
                return jsonify({"error": f"Restaurant with ID {restaurant_id} not found"}), 404

            
            new_restaurant_pizza = RestaurantPizza(
                pizza_id=pizza_id,
                restaurant_id=restaurant_id,
                price=price
            )

            db.session.add(new_restaurant_pizza)
            db.session.commit()

            return jsonify({"message": "Pizza added to restaurant's menu successfully"}), 201

        except Exception as e:
            return jsonify({"error": "Error occurred"}), 500




if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(port=5000, debug=True)
