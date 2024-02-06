from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import os
import json

app = Flask(__name__)
CORS(app, resources={r"/process*": {"origins": "http://localhost:3000"}})

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'data', 'smpl')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/process', methods=['GET'])
def process_gender():
    gender = request.args.get('gender', '').upper()

    if gender not in ['MALE', 'FEMALE', 'NEUTRAL']:
        return jsonify({'error': 'Invalid gender'}), 400

    try:
        run_script_path = os.path.join(ROOT_DIR, 'run.py')
        # Ensure run.py outputs JSON-formatted string
        result = subprocess.run(['python', run_script_path, gender], check=True, stdout=subprocess.PIPE, text=True)
        output = result.stdout

        # Find the first JSON object
        json_start = output.find('{')
        json_end = output.rfind('}') + 1
        json_str = output[json_start:json_end]
        measurements = json.loads(json_str)

    except subprocess.CalledProcessError as e:
        print(f"Failed to execute run.py: {e}")
        return jsonify({'error': f"Error executing script: {e}"}), 500
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON output: {e}")
        return jsonify({'error': f"Error parsing output: {e}"}), 500

    return jsonify({'Measurements': measurements}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    print(f"Saving files to: {os.path.abspath(UPLOAD_FOLDER)}")

    if 'file' not in request.files or 'gender' not in request.form:
        return 'File or gender parameter missing in the request', 400

    file = request.files['file']
    gender = request.form['gender'].upper()

    if gender not in ['MALE', 'FEMALE', 'NEUTRAL']:
        return 'Invalid gender', 400

    if file.filename == '':
        return 'No selected file', 400

    if file and file.filename.endswith('.pkl'):
        filename = f'SMPL_{gender}.pkl'  # Rename the file based on gender
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)

        try:
            run_script_path = os.path.join(ROOT_DIR, 'run.py')
            subprocess.run(['python', run_script_path, gender], check=True)
            print("run.py executed successfully")
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute run.py: {e}")
            return f"Error executing script: {e}", 500

        return f'File saved to {save_path}', 200
    else:
        return 'Invalid file type', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
