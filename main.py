from flask import Flask, jsonify, request, render_template
import random
import string
import time
import requests

app = Flask(__name__)

codes = {}

def generate_code(length=64):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/generate_code', methods=['GET'])
def generate_and_display_code():
    code = generate_code()
    expiration_time = time.time() + 120
    codes[code] = expiration_time
    return jsonify({'code': code, 'message': 'comment this code on <a href="https://cocrea.world/@PuzzlingGGG/CocreaAuth">cocrea.world/@PuzzlingGGG/CocreaAuth</a> without ANYTHING ELSE!'})

@app.route('/verify_code', methods=['POST'])
def verify_code():
    input_code = request.json.get('code')
    if input_code in codes and codes[input_code] > time.time():
        response = requests.get('https://api.cocrea.world/creation-comments?creationId=1766942744927846401&page=1&perPage=20&sortField=id&sortType=DESC')
        comments = response.json().get('body', {}).get('data', [])
        for comment in comments:
            if input_code in comment.get('content', ''):
                return jsonify({'status': 'success', 'message': 'authentication successful', 'username': comment['commenter']['username'], 'id': comment['commenter']['id']})
        return jsonify({'status': 'failure', 'message': 'code not found in comments'})
    else:
        return jsonify({'status': 'failure', 'message': 'invalid or expired code'})

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
