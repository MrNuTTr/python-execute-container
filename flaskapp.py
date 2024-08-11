from functools import wraps
import os
from flask import Flask, request
from run_and_assert import run_and_assert_code
app = Flask(__name__)

AUTH_TOKEN = os.getenv('X_AUTH_TOKEN')

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if AUTH_TOKEN == None:
            return f(*args, **kwargs)

        token = request.headers.get('X-Auth-Token')

        if not token or token != AUTH_TOKEN:
            return {'message': 'Token is missing or invalid'}, 403
        
        return f(*args, **kwargs)
    return decorated

@app.route('/run', methods=['POST'])
@token_required
def run_code():
    data = request.get_json()
    user_code = data.get('userCode')
    test_code = data.get('testCases')

    result = run_and_assert_code(user_code, test_code)

    return result


if __name__ == '__main__':
    app.run(port=8000)