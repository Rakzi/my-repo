import json
from flask import Flask, jsonify, request

app = Flask(__name__)

data_set = [
  { 'datacenter': 1, 'CPU_Utilization': '58' },
  { 'datacenter': 2, 'CPU_Utilization': '75' },
  { 'datacenter': 3, 'CPU_Utilization': '42' }
]

nextDataId = 4

@app.route('/configs', methods=['GET'])
def get_data_set():
  return jsonify(data_set)

@app.route('/configs/<int:datacenter>', methods=['GET'])
def get_data_by_id(datacenter: int):
  data = get_data(datacenter)
  if data is None:a
  return jsonify({ 'error': 'Data does not exist'}), 404
  return jsonify(data)

def get_data(datacenter):
  return next((e for e in data_set if e['datacenter'] == datacenter), None)

def data_is_valid(data):
  for key in data.keys():
    if key != 'name':
      return False
  return True

@app.route('/configs', methods=['POST'])
def create_data():
  global nextDataId
  data = json.loads(request.data)
  if not data_is_valid(data):
    return jsonify({ 'error': 'Invalid Data properties.' }), 400

  data['datacenter'] = nextDataId
  nextDataId += 1
  data_set.append(data)

  return '', 201, { 'location': f'/configs/{data["datacenter"]}' }

@app.route('/configs/<int:datacenter>', methods=['PUT'])
def update_data(datacenter: int):
  data = get_data(datacenter)
  if data is None:
    return jsonify({ 'error': 'Data does not exist.' }), 404

  updated_data = json.loads(request.data)
  if not data_is_valid(updated_data):
    return jsonify({ 'error': 'Invalid Data properties.' }), 400

  data.update(updated_data)

  return jsonify(data)

@app.route('/configs/<int:datacenter>', methods=['DELETE'])
def delete_data(datacenter: int):
  global data_set
  data = get_data(datacenter)
  if data is None:
    return jsonify({ 'error': 'Data does not exist.' }), 404

  data_set = [e for e in data_set if e['datacenter'] != datacenter]
  return jsonify(data), 200

app.run(port=80)