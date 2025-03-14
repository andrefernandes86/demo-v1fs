from flask import Flask, request, jsonify, render_template
import os
import amaas.grpc
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'exe', 'ps1', 'doc', 'docx', 'xls', 'xlsx'}
######################################
# Replace with your API KEY here!!!  #
######################################
API_KEY = 'TTin38ciSQRzzdALZVRbHjeENErTquwXO5My926nMuglWY_-MUdFsSvHZApBwAsE9pJA2Ol7OqSguSOudWURudppq2vl46iaGvKsQWAtEkTM50QOJCrLhmd79wNdF0z7Wxy8pdIOLOEdzMdXiI1qizV4Ryfx5iUHBP_otOJsrf3OwPt1cLo2XBNurdCx10hrPZHx89j6ibpty5sRTkPvz-ZAdekRE6OhPDf4oOoneTGGGbW03HTeIcwzG46AhnMlAjt0oA32l6UpGhTstGAVElHyMk7nUHhgbMOK6_FgLEMd91GC2bGkHq30K4lbv8WxVHL-W_e0Q1aKmrbs3ekJ2xXpFG3vVGaF5KVSxVUL7rj_Pb3DUsnw-gcTa1OknA7x7AyQoxBbK7ChskkgxX6SQwsC0iSWM6tJ3mF0m9wY1QYNHnvmXWy1BF6JpkEl9Ry8wGw_r3Gq9KfPW2kJPQ2R92vxI4HTDeelqyi10GvL0TwbaUvB-pd9QuTsNY_3HG_AJSiLVBVpDIH-ckjT-ofKMuBYJRc1-YTYabKw50oJfFrilfXiJMyFJ3EIbOezO3vKWSwCPPDYdTO0By_ifP2Luoyd__3lr_myuwrq358qQtv2Esw_rYhA4hdjE'
REGION = 'us-east-1'
TLS_ENABLED = False
CA_CERT = None

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the AMAAS gRPC handle
try:
    handle = amaas.grpc.init_by_region(region=REGION, api_key=API_KEY)
except Exception as e:
    print(f"Error initializing gRPC handle: {e}")
    handle = None


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'status': 'error', 'message': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # Perform file scan using AMAAS
            result = amaas.grpc.scan_file(
                channel=handle, file_name=filepath, pml=True, tags=["web_upload"], feedback=False
            )
            return jsonify({'status': 'success', 'message': 'File scanned successfully', 'result': str(result)}), 200
        except Exception as e:
            return jsonify({'status': 'error', 'message': f'Scan failed: {e}'}), 500
    else:
        return jsonify({'status': 'error', 'message': 'File type not allowed'}), 400


@app.route('/config', methods=['GET'])
def config():
    """Endpoint to verify current configuration"""
    return jsonify({
        'api_key': API_KEY,
        'region': REGION,
        'tls_enabled': TLS_ENABLED,
        'ca_cert': CA_CERT,
    })


if __name__ == '__main__':
    if handle is None:
        print("Failed to initialize gRPC handle. Please check your configuration.")
    else:
        app.run(host='0.0.0.0', port=5000)

