import unittest
import io
import sys
from flask import Flask, request
app = Flask(__name__)

def run_code_and_check_output(user_code, test_code):
    # Redirect stdout and stderr
    stdout = io.StringIO()
    stderr = io.StringIO()
    sys.stdout = stdout
    sys.stderr = stderr

    # Define the test case
    class TestUserCode(unittest.TestCase):
        pass

    # Add a test method to the test case
    setattr(TestUserCode, 'test_user_code',
            lambda self: exec(user_code + '\n' + test_code))

    # Run the test case
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUserCode)
    result = unittest.TextTestRunner().run(suite)

    # Restore stdout and stderr
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    # Return the test result and console output
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

app.run()