from flask import Flask, request, jsonify, send_file, send_from_directory
import products_dao
import uom_dao
import json
import orders_dao
from sql_connection import get_sql_connection

app = Flask(__name__)
connection = get_sql_connection()

@app.route('/', methods=['GET'])
def serve_index():
    return send_file('../ui/index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_html(path):
    return send_from_directory('../ui', path)

@app.route('/css/<path:path>', methods=['GET'])
def serve_css(path):
    return send_from_directory('../ui/css', path)

@app.route('/images/<path:path>', methods=['GET'])
def serve_images(path):
    return send_from_directory('../ui/images', path)

# Route to serve JavaScript files
@app.route('/js/<path:path>', methods=['GET'])
def serve_js(path):
    return send_from_directory('../ui/js', path)

@app.route('/getproduct', methods = ['GET'])
def get_products():
    return_id = products_dao.get_all_products(connection)
    response = jsonify({
        'product_id' : return_id
    })
    response.headers.add('Access-Controll-Allow-Origin', '*')
    return response
@app.route('/getUOM', methods = ['GET'])
def get_uom():
    response = uom_dao.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Controll-Allow-Origin','*')
    return response

@app.route('/deleteproduct', methods = ['post'])
def delete_product():
    return_id = products_dao.delete_product(connection,request.form['product_id'])
    response = jsonify({
        return_id
    })

@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = products_dao.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = orders_dao.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = orders_dao.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    print("Starting Python Flask server For Grocery Store Management System")
    app.run(port=5000)