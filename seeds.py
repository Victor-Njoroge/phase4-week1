from main import app, db, Pizza, Restaurant, RestaurantPizza
from datetime import datetime

# Create sample data for Pizzas
pizza1 = Pizza(name="Margherita", ingredients="Tomato, Mozzarella, Basil")
pizza2 = Pizza(name="Pepperoni", ingredients="Tomato, Mozzarella, Pepperoni")
pizza3 = Pizza(name="Hawaiian", ingredients="Tomato, Mozzarella, Ham, Pineapple")

# Create sample data for Restaurants
restaurant1 = Restaurant(name="Pizza Place 1", address="123 Main St")
restaurant2 = Restaurant(name="Pizza Place 2", address="456 Elm St")

# Create sample data for Restaurant_Pizza relationships
restaurant_pizza1 = RestaurantPizza(restaurant=restaurant1, pizza=pizza1, price=10)
restaurant_pizza2 = RestaurantPizza(restaurant=restaurant1, pizza=pizza2, price=12)
restaurant_pizza3 = RestaurantPizza(restaurant=restaurant2, pizza=pizza2, price=11)
restaurant_pizza4 = RestaurantPizza(restaurant=restaurant2, pizza=pizza3, price=13)

# Add the data to the database and commit the changes
with app.app_context():
    db.session.add(pizza1)
    db.session.add(pizza2)
    db.session.add(pizza3)
    db.session.add(restaurant1)
    db.session.add(restaurant2)
    db.session.add(restaurant_pizza1)
    db.session.add(restaurant_pizza2)
    db.session.add(restaurant_pizza3)
    db.session.add(restaurant_pizza4)
    db.session.commit()

print("Seed data has been added to the database.")
