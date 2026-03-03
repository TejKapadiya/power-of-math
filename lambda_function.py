import json
import math
import boto3
from time import gmtime, strftime

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('PowerOfMathDatabase')

def lambda_handler(event, context):
    """
    AWS Lambda function to calculate base^exponent,
    store the result in DynamoDB, and return the result.
    """
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',  # Allows all origins
        'Access-Control-Allow-Methods': 'OPTIONS,POST',  # Allow OPTIONS and POST methods
        'Access-Control-Allow-Headers': 'Content-Type'  # Allow Content-Type header
    }

    # Handle OPTIONS request (for CORS preflight)
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps('CORS pre-flight success')  # Empty body for OPTIONS request
        }

    try:
        # Handle POST request (actual logic)
        body = json.loads(event['body'])  # Parse the body into JSON
        base = int(body['base'])  # Convert base to an integer
        exponent = int(body['exponent'])  # Convert exponent to an integer

        # Perform the calculation: base^exponent
        math_result = math.pow(base, exponent)

        # Get the current time for DynamoDB logging
        now = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())

        # Store the result and timestamp in DynamoDB
        table.put_item(
            Item={
                'ID': str(math_result),
                'LatestGreetingTime': now
            }
        )

        # Return result in JSON format
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'body': f'Your result is {math_result}'})
        }

    except Exception as e:
        # If any error occurs, return a 500 error with the message
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }
