import unittest
import io
import sys
from flask import Flask, request
app = Flask(__name__)

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
    result = unittest.TextTestRunner().run(suite)

    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    return result.wasSuccessful(), stdout.getvalue(), stderr.getvalue()

@app.route('/run', methods=['POST'])
def run_code():
    data = request.get_json()
    user_code = data.get('userCode')
    test_code = data.get('testCode')

    success, stdout, stderr = run_code_and_check_output(user_code, test_code)

    return {
        'success': success,
        'stdout': stdout,
        'stderr': stderr
    }

if __name__ == '__main__':
    app.run()