from functools import wraps
from threading import Thread
import unittest
import io
import sys
import os
from flask import Flask, request
app = Flask(__name__)

AUTH_TOKEN = os.getenv('X_AUTH_TOKEN')

def run_code_and_check_output(user_code, test_code):
    stdout = io.StringIO()
    stderr = io.StringIO()
    sys.stdout = stdout
    sys.stderr = stderr

    class TestUserCode(unittest.TestCase):
        pass

    setattr(TestUserCode, 'test_user_code',
            lambda self: exec(user_code + '\n' + test_code))

    suite = unittest.TestLoader().loadTestsFromTestCase(TestUserCode)

    result_dict = {'success': None, 'stdout': None, 'stderr': None, 'reason': None}

    def run_tests():
        try:
            result = unittest.TextTestRunner().run(suite)
            result_dict['success'] = result.wasSuccessful()
            result_dict['stdout'] = stdout.getvalue()
            result_dict['stderr'] = stderr.getvalue()
            if result.wasSuccessful():
                result_dict['reason'] = 'success'
            else:
                result_dict['reason'] = 'error'
        except Exception as e:
            result_dict['success'] = False
            result_dict['stdout'] = stdout.getvalue()
            result_dict['stderr'] = str(e)
            result_dict['reason'] = 'error'

    t = Thread(target=run_tests)
    t.start()

    # Wait for 2 seconds or until the thread finishes
    t.join(timeout=2)

    if t.is_alive():
        result_dict['success'] = False
        result_dict['reason'] = 'timeout'

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    return result_dict['success'], result_dict['stdout'], result_dict['stderr'], result_dict['reason']

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
    test_code = data.get('testCode')

    success, stdout, stderr, reason = run_code_and_check_output(user_code, test_code)

    return {
        'success': success,
        'stdout': stdout,
        'stderr': stderr,
        'reason': reason
    }


if __name__ == '__main__':
    app.run(port=8000)