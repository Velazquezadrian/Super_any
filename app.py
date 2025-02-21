from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sync/gemini', methods=['POST'])
def sync_gemini():
    data = request.get_json()
    pregunta = data['pregunta']
    response = requests.post('http://localhost:5000/sync/gemini', json={"content": pregunta})
    return jsonify(response.json())

@app.route('/sync/copilot', methods=['POST'])
def sync_copilot():
    data = request.get_json()
    pregunta = data['pregunta']
    response = requests.post('http://localhost:5000/sync/copilot', json={"content": pregunta})
    return jsonify(response.json())

@app.route('/sync/llama3_2', methods=['POST'])
def sync_llama3_2():
    data = request.get_json()
    pregunta = data['pregunta']
    response = requests.post('http://localhost:5000/sync/llama3_2', json={"content": pregunta})
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True)

