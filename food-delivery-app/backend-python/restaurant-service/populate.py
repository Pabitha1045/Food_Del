from app import db, Restaurant, app

with app.app_context():
    # Clear existing data
    db.session.query(Restaurant).delete()
    db.session.commit()

    # Add sample restaurants
    restaurants = [
        Restaurant(name='Pizza Palace', address='123 Main St', phone='555-1234'),
        Restaurant(name='Burger Barn', address='456 Oak Ave', phone='555-5678'),
    ]

    for restaurant in restaurants:
        db.session.add(restaurant)

    db.session.commit()
    print('Sample restaurants added')
