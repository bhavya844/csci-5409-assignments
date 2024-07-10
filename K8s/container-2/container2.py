from flask import Flask, jsonify, request
import csv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.json.sort_keys = True

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    file = data.get('file')
    product = data.get('product')
    file_path = f"../bhavya_PV_dir/{file}"

    # Log the obtained values
    logging.info(f"Received request with file: {file}, product: {product}")
    logging.info(f"File path resolved to: {file_path}")

    total_amount = 0

    try:
        with open(file_path, mode='r') as csvfile:
            csv_reader = csv.DictReader(csvfile)
            
            # Normalize headers to strip any leading/trailing spaces
            csv_reader.fieldnames = [field.strip() for field in csv_reader.fieldnames]

            rows_found = False
            for row in csv_reader:
                # Normalize row keys to strip any leading/trailing spaces
                row = {key.strip(): value for key, value in row.items()}
                
                if row['product'] == product:
                    total_amount += int(row['amount'])
                    rows_found = True
            
            if not rows_found:
                logging.warning(f"No rows found for product: {product} in file: {file_path}")
                return jsonify({"file": file, "error": "Input file not in CSV format."}), 400
            
            return jsonify({"file": file, "sum": total_amount})
    
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return jsonify({"file": file, "error": "File not found."}), 404
    
    except KeyError as e:
        logging.error(f"Key error: {str(e)}")
        return jsonify({"file": file, "error": f"Column {str(e)} not found in the file."}), 400
    
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return jsonify({"file": file, "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
