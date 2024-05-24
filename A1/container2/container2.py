from flask import Flask, request, jsonify
import csv

app = Flask(__name__)
app.json.sort_keys = False


@app.route('/process', methods=['POST'])
def process():
    data=request.get_json()
    file=data.get('file')
    product=data.get('product')
    file_path=f"/storage/{file}"
    total_amount=0
    count=0

    with open(file_path, mode='r') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        total_amount = 0
        count = 0
        rows_found = False
        for row in csv_reader:
            count += 1       
            if row['product'] == product:
                total_amount += int(row['amount'])
                rows_found = True
        if not rows_found :
            return jsonify({"file": file, "error": "Input file not in CSV format."})
        return jsonify({"file": file, "sum": total_amount})

    
if __name__=='__main__':
    app.run(host='0.0.0.0',port=7000)


