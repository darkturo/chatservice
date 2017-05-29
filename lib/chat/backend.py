import json

from flask import request

from chat import app

@app.route('/api/v.0.1/test', methods=['POST'])
def test():
    return json.dumps({'status': 'ok'}), 200
