from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = "sqlite:///./orders.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Table
class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    item = Column(String)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "API is working with DB"}

@app.post("/add-order")
def add_order(customer_name: str, item: str):
    db = SessionLocal()
    new_order = Order(customer_name=customer_name, item=item)
    db.add(new_order)
    db.commit()
    db.close()
    return {"message": "Order saved in database"}

@app.get("/orders")
def get_orders():
    db = SessionLocal()
    orders = db.query(Order).all()
    db.close()
    return orders

@app.get("/repeat-customers")
def repeat_customers():
    db = SessionLocal()
    orders = db.query(Order).all()
    
    count = {}
    for order in orders:
        name = order.customer_name
        count[name] = count.get(name, 0) + 1
    
    repeat = [name for name, c in count.items() if c > 1]
    
    db.close()
    return {"repeat_customers": repeat}

@app.get("/analytics")
def analytics():

    db = SessionLocal()

    orders = db.query(Order).all()

    total_orders = len(orders)

    customers = set()
    items = {}

    for order in orders:

        customers.add(order.customer_name)

        if order.item in items:
            items[order.item] += 1
        else:
            items[order.item] = 1

    if items:
        most_ordered_item = max(items, key=items.get)
    else:
        most_ordered_item = "No Orders"

    db.close()

    return {
        "total_orders": total_orders,
        "total_customers": len(customers),
        "most_ordered_item": most_ordered_item
    }
    
@app.get("/search-customer")
def search_customer(name: str):

    db = SessionLocal()

    orders = db.query(Order).filter(Order.customer_name == name).all()

    db.close()

    return orders

@app.get("/customer-status")
def customer_status():

    db = SessionLocal()

    orders = db.query(Order).all()

    count = {}

    for order in orders:
        name = order.customer_name
        count[name] = count.get(name, 0) + 1

    status = {}

    for name, total in count.items():

        if total >= 5:
            status[name] = "Loyal Customer"

        elif total >= 2:
            status[name] = "Repeat Customer"

        else:
            status[name] = "Normal Customer"

    db.close()

    return status