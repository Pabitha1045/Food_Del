from app import db, Restaurant, MenuItem, app

with app.app_context():
    # Add sample restaurants
    restaurant1 = Restaurant(name='Pizza Palace', address='123 Main St', phone='555-1234')
    restaurant2 = Restaurant(name='Burger Barn', address='456 Oak Ave', phone='555-5678')
    db.session.add(restaurant1)
    db.session.add(restaurant2)
    db.session.commit()

    # Add menu items
    menu1 = MenuItem(restaurant_id=restaurant1.id, name='Margherita Pizza', description='Classic cheese pizza', price=12.99)
    menu2 = MenuItem(restaurant_id=restaurant1.id, name='Pepperoni Pizza', description='Pepperoni pizza', price=14.99)
    menu3 = MenuItem(restaurant_id=restaurant2.id, name='Cheeseburger', description='Juicy cheeseburger', price=9.99)
    menu4 = MenuItem(restaurant_id=restaurant2.id, name='Fries', description='Crispy fries', price=4.99)

    db.session.add(menu1)
    db.session.add(menu2)
    db.session.add(menu3)
    db.session.add(menu4)
    db.session.commit()

    print('Sample data added successfully!')
