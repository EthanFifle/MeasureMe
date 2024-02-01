from flask import Flask, request
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(ROOT_DIR, 'data', 'smpl')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/process', methods=['GET'])
def process_gender():
    gender = request.args.get('gender', '').upper()

    if gender not in ['MALE', 'FEMALE', 'NEUTRAL']:
        return 'Invalid gender', 400

    try:
        run_script_path = os.path.join(ROOT_DIR, 'run.py')
        result = subprocess.run(['python', run_script_path, gender], check=True, stdout=subprocess.PIPE, text=True)
        output = result.stdout
        print("run.py executed successfully with gender:", gender)
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute run.py: {e}")
        return f"Error executing script: {e}", 500

    return output, 200

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
