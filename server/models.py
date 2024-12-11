from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    reviews = db.relationship('Review', back_populates='customer')
    items = association_proxy('reviews', 'item')
    _exclude_columns = ('reviews',)



    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'

class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    reviews = db.relationship('Review', back_populates='item')
    _exclude_columns = ('reviews',)

    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    
    customer = db.relationship('Customer', back_populates='reviews')
    item = db.relationship('Item', back_populates='reviews')
    _exclude_columns = ('customer', 'item')

    def __repr__(self):
        return f'<Review {self.id}, {self.comment}>'

    @staticmethod
    def create_review(app):
        with app.app_context():
            customer = Customer(name='John Doe')
            item = Item(name='Laptop', price=999.99)

            db.session.add(customer)
            db.session.add(item)
            db.session.commit()

            review = Review(comment='Great product!', customer_id=customer.id, item_id=item.id)

            db.session.add(review)
            db.session.commit()

            saved_review = Review.query.get(review.id)
            print(saved_review)
