from flask import Flask, render_template, request, jsonify
from config_generator import generate_vpn_config

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    config = generate_vpn_config(data)
    return jsonify({"config": config})

if __name__ == '__main__':
    app.run(debug=True)