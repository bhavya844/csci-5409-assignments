import csv
from flask import Flask, request, jsonify
import requests
import os

app=Flask(__name__)
app.json.sort_keys = True

persistent_storage_path="../bhavya_PV_dir"

if not os.path.exists(persistent_storage_path):
    os.makedirs(persistent_storage_path)


@app.route('/calculate', methods=['POST'])
def calculate():
    data=request.get_json()
    file=data.get('file')
    print(file)
    product=data.get('product')

    if file is None:
        return jsonify({"file": None, "error": "Invalid JSON input."}), 404

    file_path=f"../bhavya_PV_dir/{file}"
    
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
    
    response=requests.post('http://app2-service:8081/process', json={"file": file, "product": product})
    return jsonify(response.json())

@app.route('/store-file',methods=['POST'])
def store_file():
    data=request.get_json()
    file=data.get('file')

    file_path = f"../bhavya_PV_dir/{file}"
    try:
        if request.json["file"]==None:
            return jsonify({"file":None,"error": "Invalid JSON input."}), 404
    except KeyError:
        return jsonify({"file":None,"error": "Invalid JSON input."}), 404
    
    try:
        # with open("/bhavya_pv/"+request.json["file"],"w+") as csvfile:
        with open(file_path,"w+") as csvfile:
            csvfile.write(request.json["data"].replace("\\n","\n"))
    except Exception as e:
        return jsonify({"file":request.json["file"],"error": "Error while storing the file to the storage."}),400

    return jsonify({"file":request.json["file"],"message":"Success."}),200


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, debug=True)