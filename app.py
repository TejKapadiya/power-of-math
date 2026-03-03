# This Python file is designed to run as a Flask web service on an EC2 instance.
# It calculates the result of raising a base number to an exponent (base^exponent) 
# and stores the result along with a timestamp in an AWS DynamoDB table named 'PowerOfMathDatabase'.
# The Flask app listens for POST requests with JSON data containing 'base' and 'exponent'.
# Once the result is calculated, it is stored in DynamoDB, and a JSON response with the result  is sent back to the client.
# This file can be triggered by an SPA frontend function deployed on same or diffrent EC2 instance with Flask serving as the web framework to handle incoming requests.
import json
import math
import boto3
from time import gmtime, strftime
from flask import Flask, request, jsonify

# Initialize Flask app to create a web server
app = Flask(__name__)

# Initialize DynamoDB resource to interact with AWS DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PowerOfMathDatabase')  # DynamoDB table where results will be stored

@app.route('/', methods=['POST'])
def calculate():
    """
    Flask route to calculate base^exponent, 
    store the result in DynamoDB, and return the result.
    This function is designed to be triggered as a Lambda function.
    
    - Accepts POST requests with 'base' and 'exponent' values in JSON format.
    - Computes base raised to the power of exponent.
    - Stores the result and timestamp in DynamoDB.
    - Returns a JSON response with the calculated result.
    """
    try:
        # Get the data from the request body (JSON)
        data = request.get_json()

        # Extract the 'base' and 'exponent' values from the received JSON
        base = int(data['base'])
        exponent = int(data['exponent'])

        # Get the current time (formatted)
        now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        # Perform the calculation of base^exponent
        math_result = math.pow(base, exponent)

        # Store the result and timestamp in DynamoDB
        table.put_item(
            Item={
                'ID': str(math_result),  # Use the result as a unique ID for the item
                'LatestGreetingTime': now  # Store the current time of calculation
            }
        )

        # Return the result as a JSON response
        return jsonify({'body': f'Your result is {math_result}', 'status': 'success'}), 200

    except Exception as e:
        # Handle any errors and return the error message as JSON
        return jsonify({'message': str(e), 'status': 'error'}), 400

# Start the Flask app, making it accessible on all IP addresses of the EC2 server
if __name__ == '__main__':
    # Uncomment the following line for local development debugging
    # app.run(debug=True)

    # Run the Flask app on all available network interfaces of the EC2 server (0.0.0.0)
    # and make it available on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
