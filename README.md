# Repeat Customer Insights Portal

## Project Description
Repeat Customer Insights Portal is a restaurant intelligence system developed to track returning customers, analyze order patterns, and identify customer loyalty trends.

This project helps restaurants understand customer behavior using backend APIs and database integration.

---

## Features
- Add customer orders
- Store orders in database
- View all orders
- Identify repeat customers
- Simple frontend UI
- FastAPI Swagger API testing

---

## Technologies Used
- FastAPI
- Python
- SQLite
- SQLAlchemy
- HTML
- CSS
- JavaScript

---

## API Endpoints

### GET /
Checks whether API is working.

### POST /add-order
Adds customer order data.

### GET /orders
Displays all orders stored in database.

### GET /repeat-customers
Displays customers who ordered more than once.

---

## How to Run the Project

### Step 1
Install dependencies:

```bash
pip install fastapi uvicorn sqlalchemy
