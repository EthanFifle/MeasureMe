from flask import Flask, request, jsonify
from techpack import measure_body
import os
import json

app = Flask(__name__)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/betas', methods=['POST'])
def upload_info():
    if 'gender' not in request.form or 'betas' not in request.form:
        return 'Gender or betas parameter missing in the request', 400

    gender = request.form['gender'].upper()
    betas = request.form['betas']  # This is assumed to be a JSON string

    # Validate gender
    if gender not in ['MALE', 'FEMALE', 'NEUTRAL']:
        return 'Invalid gender', 400

    # Validate betas (optionally, you might want to add more robust checks here)
    try:
        betas_json = json.loads(betas)
        # Add a check to ensure betas_json is in the expected format
        if not isinstance(betas_json, list) or not all(isinstance(item, list) for item in betas_json):
            return 'Invalid betas format', 400
    except json.JSONDecodeError:
        return 'Betas must be a valid JSON string', 400

    measurements_json = measure_body(gender, betas_json)
    print("Measurements returned:", measurements_json)

    return jsonify(measurements=measurements_json)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
