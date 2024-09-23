from flask import Flask, request, session, jsonify

from DBConnection import Db

app = Flask(__name__)
app.secret_key = "1234567"

static_path = "D:\\Riss\\Projects\\snmi_app\static\\"
import os
from datetime import datetime
from flask import request, jsonify


@app.route('/add_product', methods=['POST'])
def add_product():
    # Collect form data
    userName = request.form["userName"]
    dataBase = request.form["dataBase"]
    itemCode = request.form["itemCode"]
    itemDesc = request.form["itemDesc"]
    arabicDecs = request.form["arabicDecs"]
    salesPrice = request.form["salesPrice"]
    unitCode = request.form["unitCode"]

    # Initialize barcode path as empty
    path = ""

    # Check if the file 'barCode' is in the request
    if 'barCode' in request.files:
        barCode = request.files['barCode']

        if barCode.filename != "":
            # Create a timestamped file name
            date = datetime.now().strftime('%Y%m%d-%H%M%S')
            filename = date + ".jpg"

            # Define the static path
            static_path = os.path.join(app.root_path, 'static', 'barcodeImage')

            # Ensure the directory exists
            if not os.path.exists(static_path):
                os.makedirs(static_path)

            # Full file path
            full_path = os.path.join(static_path, filename)

            # Save the file manually
            with open(full_path, 'wb') as f:
                f.write(barCode.read())

            # Set the relative URL path for the saved file
            path = "/static/barcodeImage/" + filename

            # Insert data into the database
            db = Db(user=userName, database=dataBase)
            qry = """
                INSERT INTO `products` 
                (`itemCode`, `itemDescription`, `arabicDescription`, `salesPrice`, `barcCode`, `unitCode`) 
                VALUES ('{}', '{}', '{}', '{}', '{}', '{}')
            """.format(itemCode, itemDesc, arabicDecs, salesPrice, path, unitCode)

            res = db.insert(qry)

            # Return response
            return jsonify(status="OK", data=res)

    else:
        return  jsonify(status="Error")


@app.route('/get_barcode/<itemCode>', methods=['GET'])
def get_barcode(itemCode):
    # Extract userName and dataBase from request headers
    userName = request.headers.get('userName')
    dataBase = request.headers.get('dataBase')

    if not userName or not dataBase:
        return jsonify({'error': 'userName or dataBase missing in headers'}), 400

    try:
        # Assuming you are using some kind of database connection utility Db
        db = Db(user=userName, database=dataBase)

        # Query the product table with itemCode
        query = f"SELECT * FROM products WHERE itemCode = '{itemCode}'"
        result = db.selectOne(query)

        # Check if the result exists
        if not result:
            return jsonify({'error': 'Product not found'}), 404

        # Return the result as a JSON response
        return jsonify({'product': result}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(debug = True, host="0.0.0.0",port=4000)
