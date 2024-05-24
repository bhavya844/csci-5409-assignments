import csv
from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)
app.json.sort_keys = False


@app.route('/calculate', methods=['POST'])
def calculate():
    data=request.get_json()
    file=data.get('file')
    print(file)
    product=data.get('product')

    if file is None:
        return jsonify({"file": "null", "error": "Invalid JSON input."}), 404

    file_path=f"/storage/{file}"
    # try:
    #     if not os.path.exists(file_path):
    #         return jsonify({f"file": {file}, "error": "File not found."})
    # except FileNotFoundError:
    #     return jsonify({f"file": {file}, "error": "File not found."}), 404
        
    try:
        with open(file_path, mode='r') as csvfile:
            sample = csvfile.read(1024)
            csvfile.seek(0)  
            sniffer = csv.Sniffer()
            try:
                dialect = sniffer.sniff(sample)
                if dialect.delimiter != ',':
                    return jsonify({"file": file, "error": "Input file not in CSV format."}), 400
            except csv.Error:
                return jsonify({"file": file, "error": "Input file not in CSV format."}), 400

    except FileNotFoundError:
        return jsonify({"file": f"{file}", "error": "File not found."}), 404
    
    response=requests.post('http://container2:7000/process', json={"file": file, "product": product})
    return jsonify(response.json())


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=6000)