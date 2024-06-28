from flask import Flask, request, jsonify
import mysql.connector
from config import DB_CONFIG

app = Flask(__name__)

# Establish database connection
def get_db_connection():
    return mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database']
    )

# Endpoint to store products
@app.route('/store-products', methods=['POST'])
def store_products():
    data = request.get_json()
    products = data.get('products', [])

    conn = get_db_connection()
    cursor = conn.cursor()

    for product in products:
        name = product['name']
        price = product['price']
        availability = bool(product['availability'])  # Ensure the received availability is converted to boolean
        cursor.execute(
            "INSERT INTO products (name, price, availability) VALUES (%s, %s, %s)",
            (name, price, availability)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Success."}), 200

# Endpoint to list products
@app.route('/list-products', methods=['GET'])
def list_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT name, price, availability FROM products")
    products = cursor.fetchall()

    # Convert availability to boolean in the output
    for product in products:
        product['availability'] = bool(product['availability'])

    cursor.close()
    conn.close()

    return jsonify({"products": products}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)