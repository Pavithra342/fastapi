from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
import string

# Define the SQLAlchemy base
Base = declarative_base()

# Define the Product model
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    image = Column(String, nullable=False)
    attributes = Column(Text)
    offer = Column(String)
    reviews = Column(Text)

# Create an SQLite database engine
engine = create_engine('sqlite:///products.db')

# Create the products table
Base.metadata.create_all(engine)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

# Generate 10,000 random product records and add them to the session
products = []
for i in range(10000):
    name = ''.join(random.choices(string.ascii_lowercase, k=10))
    price = round(random.uniform(10, 1000), 2)
    image = f"image_{i}.png"
    attributes = ', '.join(random.sample(["Cotton", "Regular Fit", "15.6\" Display", "8GB RAM", "Android", "Adjustable height and armrests", "Lumbar support"], random.randint(1, 3)))
    offer = random.choice(["20% off", "Free carrying case", "20% off", None])
    reviews = ', '.join(random.sample(["Very comfortable!", "Great for casual wear", "Powerful performance", "Battery life could be better", "Good Product", "Great for use", "This chair has saved my back! So comfortable for long workdays.", "Easy to assemble and very sturdy.", "A bit pricey, but definitely worth the investment."], random.randint(1, 3)))

    product = Product(
        name=name,
        price=price,
        image=image,
        attributes=attributes,
        offer=offer,
        reviews=reviews
    )
    products.append(product)

# Add all products to the session and commit
session.bulk_save_objects(products)
session.commit()

# Close the session
session.close()
